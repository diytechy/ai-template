"""integrate.py — the station protocol and its merge slot.

One of four modules `WI-521` slice 2 carved out of the 3,520-line
`test_integrate.py` monolith (M-06); the family and the rule for what is shared
are in `tests/integrate_fixtures.py`. This module keeps the monolith's original
subject: the backend of the one integration flow
(docs/concurrency-restructure.md §1.2), rebuilt by WI-386 on ONE constraint
(docs/concurrency-v2.md §A2) — **a branch may not enter the merge queue unless
trunk is already an ancestor of it.** The lane-side `refresh` makes that true
(merge trunk in, trunk_step, bar, commit) and the slot verifies it.

What is pinned here, beyond the gates that live in `test_integrate_admission.py`,
is that the constraint is really load-bearing rather than merely documented:

  * **the constraint itself** — `trunk_is_ancestor` and `_merge_ready`, the two
    reads the slot makes, each proven to have two answers on a topology the
    test constructs;
  * **the refresh sequence AND its order** — merge trunk -> trunk_step -> bar ->
    commit, pinned by stub harness scripts that record the order they ran in, so
    a reordering is a failure rather than a silent change of meaning;
  * **the disposable-commit rule** (§A2.1) — a second refresh RESETS to the last
    work commit and redoes the merge; it never stacks, because docs/log.md is
    append-compiled and a stack would conflict on the file end;
  * **every refresh failure leaves the branch at its last work commit, clean** —
    a conflicting trunk merge and a red bar both, so nothing is ever parked;
  * **the slot has exactly one acquisition site** (§A2.0 requirement 1), asserted
    against the source, because "restricting to pessimistic is a one-line move"
    is only true while that stays true;
  * **the pessimistic path is not dead code** — a two-branch drain reaches it by
    construction, since the first merge moves trunk out from under the second;
  * **the attestation cannot be forged** — a hand-written bar-green trailer, an
    amended refresh commit, and a work commit that merely QUOTES the trailer.

THE TWO KINDS OF BAR IN THIS MODULE ARE A DELIBERATE SPLIT, stated because a
reader who misses it will think one of them is cheating. The end-to-end test
stands in the REAL bar: a bootstrapped scaffold with a traced SN->SR->LLR->TC
chain whose `check.py --tier smoke` genuinely passes on the refreshed branch, and
`_run_bar` is never monkeypatched — a stubbed bar is exactly the vacuous green
this script exists to make impossible. The station-protocol tests use STUB
harness scripts instead, and that is a different claim, made honestly: they
measure ORDER and TOPOLOGY (which script ran when, which commit has which
parents), which a real 11-minute bar would measure no better and far more
slowly. The real bar is still the one that decides green, in the e2e.

`integrate()` itself is only ever run as a SUBPROCESS here, for the reason
`tests/test_integrate.py` states: it takes the process-global coordinator lock
fd, so an in-process call would leak a held descriptor into the rest of the
suite.
"""

import re

from conftest import SCRIPTS, env_gate_skipif, run_py
from integrate_fixtures import (
    T_CODE,
    T_LATER,
    T_VERDICT,
    VERDICT_APPROVE,
    _branches,
    _commit,
    _git,
    _rev,
    _worktree_count,
    claim_repo,
    declare_generated,
    integ,
    scaffolded_closed_branch,
    write_spec,
)

pytestmark = env_gate_skipif("git")


# --- 5b. THE STATION PROTOCOL (WI-386) ---------------------------------------
#
# The one constraint, the refresh that satisfies it, and the two properties the
# owner's caveat turned into requirements. Every fixture below CONSTRUCTS the
# topology it measures — two branches cut from one base, a trunk that moves
# under a finished branch — rather than inheriting a repo's state, because the
# thing under test is a relationship between commits.

# A stub harness pair, written INTO the branch tree so `_branch_tree_script`
# finds it there. Each appends its own name to a `harness-order.txt` that sits
# OUTSIDE the worktree — the refresh sheds the residue its own bar leaves, and
# rightly, so a recorder placed inside the tree would be swept away by the very
# behaviour it is there to record. That file is what makes the ORDER assertion
# possible at all: the real bar can say "green", but only a recording stub can
# say "and I ran after the trunk step".
STUB_TRUNK_STEP = """import pathlib

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "trunk_step\\n"
)
pathlib.Path("regenerated.txt").write_text("fresh\\n", encoding="utf-8")
"""

STUB_CHECK_GREEN = """import pathlib
import sys

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "check " + " ".join(sys.argv[1:]) + "\\n"
)
pathlib.Path("bar-cache").mkdir(exist_ok=True)
pathlib.Path("bar-cache", "run.txt").write_text("a tool cache\\n", encoding="utf-8")
print("  PASS  format           0.1s")
print("  PASS  tests+coverage   0.2s")
"""

STUB_CHECK_RED = """import pathlib
import sys

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "check-red\\n"
)
print("=== format : stub ruff format --check ===")
print("  PASS  format           0.1s")
print("=== tests+coverage : stub pytest -q ===")
print("FAILED tests/test_widget.py::test_value - AssertionError: VALUE")
print("1 failed, 3 passed in 0.2s")
print("  FAIL  tests+coverage   exit 1 (0.2s)")
print("=" * 56)
print("Check summary (gate DevStg-Impl, tier smoke):")
print("  PASS  format           0.1s")
print("  FAIL  tests+coverage   exit 1 (0.2s)")
print("=" * 56)
print("RESULT: FAIL (1 step(s) failed)")
sys.exit(1)
"""


def station_repo(
    tmp_path,
    check_src=STUB_CHECK_GREEN,
    policy="0",
    dest="complete",
    product=True,
    **spec_kw,
):
    """A trunk with WI-401 claimed onto `wi-401` and CLOSED, plus a stub harness.

    Everything the slot reads is real: a real claim commit, a real branch, a
    real closing move. Only the two harness scripts are stubs, and they are
    stubs so the test can assert the ORDER they ran in — see above. `spec_kw`
    shapes the claimed spec (the WI-388 bar/no-bar tests declare `bar=` or
    `safety=` on it); `product=False` closes the lane WITHOUT the product
    file, the pure-registry shape an honest adjudication lane has.
    """
    root = claim_repo(tmp_path, **spec_kw)
    (root / ".gitignore").write_text(
        "out/\nbar-cache/\n", encoding="utf-8", newline="\n"
    )
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n", encoding="utf-8", newline="\n"
    )
    declare_generated(root)
    (root / "docs" / "review-policy").write_text(
        policy + "\n", encoding="utf-8", newline="\n"
    )
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(check_src, encoding="utf-8", newline="\n")
    _commit(root, "chore: the stub harness and the declared bar", when=T_CODE)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    close_branch(root, "wi-401", dest=dest, product=product)
    return root


def close_branch(
    root, branch, wi="WI-401", slug="widget", extra=None, dest="complete", product=True
):
    """Build and CLOSE `branch` in its own lane worktree: one product commit and
    the §2.3 step-3 move to its TERMINAL directory. Leaves the worktree
    registered, which is where the refresh will run — the lane's own tree, by
    design. (WI-384 split `archive/` into `complete/` + `cancelled/`; the
    finished signal is unchanged — the tree no longer holds a spec under
    `active/<branch>/` — but the destination has to be a real state folder or
    the loaders refuse it.)"""
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / branch
    _git(root, "worktree", "add", "-q", str(wt), branch)
    if product:
        (wt / "{}.txt".format(branch)).write_text("1\n", encoding="utf-8", newline="\n")
    dst = wt / "docs" / "work" / dest / "{}-{}.md".format(wi, slug)
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = wt / "docs" / "work" / "active" / branch / "{}-{}.md".format(wi, slug)
    dst.write_text(
        src.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
        encoding="utf-8",
        newline="\n",
    )
    _git(wt, "rm", "-q", "docs/work/active/{}/{}-{}.md".format(branch, wi, slug))
    if extra:
        (wt / extra[0]).write_text(extra[1], encoding="utf-8", newline="\n")
    _commit(wt, "{}: build + close".format(wi), when=T_VERDICT)
    return wt


def _lane(root, branch):
    """The lane worktree path `station_repo`/`close_branch` put the branch in."""
    return root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / branch


def _order(wt):
    path = wt.parent / "harness-order.txt"
    return path.read_text(encoding="utf-8").split() if path.is_file() else []


def _refresh_commits(root, branch):
    """Every commit on `branch` carrying the bar-green trailer, tip-first."""
    out = _git(root, "log", "--format=%H%x1f%B%x1e", branch).split("\x1e")
    hits = []
    for entry in out:
        if not entry.strip():
            continue
        sha, _, body = entry.strip().partition("\x1f")
        if integ.BAR_GREEN in body:
            hits.append(sha)
    return hits


# 5b.1 — the constraint itself


def test_trunk_is_ancestor_has_two_answers_on_a_constructed_topology(tmp_path):
    # THE one line the whole design rests on, proven to discriminate. The branch
    # is cut from trunk (ancestor: yes); then trunk moves (ancestor: no). If this
    # read were vacuously true the slot would merge anything.
    root = station_repo(tmp_path)
    assert integ.trunk_is_ancestor(root, "wi-401")

    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves under the finished branch", when=T_LATER)
    assert not integ.trunk_is_ancestor(root, "wi-401")


def test_merge_ready_needs_the_ancestor_relation_AND_the_attestation(tmp_path):
    # Ancestry alone says nothing about whether anyone barred the composition,
    # so the tip must also carry the bar's own trailer. Both halves are shown
    # failing separately, then passing together — a single-answer gate is not a
    # gate.
    root = station_repo(tmp_path)
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why  # ancestor ok

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    ready, why = integ._merge_ready(root, "wi-401")
    assert ready and "PASS" in why

    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves after the refresh", when=T_LATER)
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "is not an ancestor of it" in why
    assert sha == _rev(root, "wi-401")  # the attestation is still there; trunk moved


# 5b.2 — the refresh, and the order inside it


def test_the_refresh_merges_trunk_in_regenerates_bars_then_commits(tmp_path):
    # The order is FIXED and load-bearing (§A2.1): the compile has to see the
    # trunk's log before it appends, and the bar has to see what the compile and
    # the regen wrote. Asserted by recording stubs rather than by reading the
    # source, so a reordering fails here instead of passing quietly.
    root = station_repo(tmp_path)
    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves under the finished branch", when=T_LATER)
    trunk = _rev(root, "HEAD")
    work_tip = _rev(root, "wi-401")
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal

    # 1. the harness ran in the declared order, and the bar was told to stand in
    #    the TRUNK lane (the freshness gates it just regenerated must run).
    assert _order(wt)[0] == "trunk_step"
    assert "check" in _order(wt) and "--trunk-lane" in _order(wt)
    assert _order(wt).index("trunk_step") < _order(wt).index("check")
    # 2. the refresh commit is a real MERGE of trunk into the branch's work tip.
    parents = _git(root, "rev-list", "--parents", "-n", "1", sha).split()
    assert parents[1:] == [work_tip, trunk], parents
    # 3. trunk is now an ancestor — which is the entire point of the operation.
    assert integ.trunk_is_ancestor(root, "wi-401")
    # 4. ...and the tree carries what the trunk step wrote, so the bar barred it.
    assert (wt / "regenerated.txt").is_file()
    assert "regenerated.txt" in _git(root, "ls-tree", "-r", "--name-only", sha)


def test_the_refresh_attests_the_bar_to_the_sha_it_produced(tmp_path):
    # "Attested to a TREE, not to a run" (§A2): the trailer lives in the commit,
    # so the slot verifies a property of the sha rather than someone's claim
    # about a run. A later commit on the branch therefore REVOKES it, because
    # the tip is no longer the tree that was barred.
    root = station_repo(tmp_path)
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert integ.refresh_attestation(root, "wi-401", sha)
    assert integ.refresh_attestation(root, "wi-401")

    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    (wt / "afterthought.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: one more idea", when=T_LATER)
    assert integ.refresh_attestation(root, "wi-401") is None
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why


def test_the_bar_residue_the_refresh_created_is_shed_but_the_lanes_is_not(tmp_path):
    # The refresh leaves the lane worktree as it found it plus one commit. It
    # sheds the IGNORED residue its own bar wrote (or §5.6's unload would refuse
    # to GC the lane over caches the integrator itself created), and touches
    # nothing that was there before — the `out/run-logs/` stream WI-359 names
    # must still block the unload.
    root = station_repo(tmp_path)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    logs = wt / "out" / "run-logs"
    logs.mkdir(parents=True)
    (logs / "session.md").write_text("the only copy\n", encoding="utf-8", newline="\n")

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert (wt / "bar-cache").is_dir() is False, "the bar's own residue stays"
    assert (logs / "session.md").read_text(encoding="utf-8") == "the only copy\n"


# 5b.2-wi388 — the adjudication no-bar arm and the `bar` strictness key


def test_the_merge_slot_mints_the_adjudication_row_at_intake(tmp_path):
    # WI-388's post-merge arm, end to end through the slot: the merged branch
    # amended an approved SR cell of an Approved row without the flip, so the
    # intake mints ONE adjudication row as its own bookkeeping commit inside
    # the same held slot — serial by construction, derived description, no
    # model in the path (§A5.2; rulings R1/R3).
    root = claim_repo(tmp_path)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    sr_header = (
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
    )
    (req / "system-requirements.csv").write_text(
        sr_header + 'SR-001,Adder,SN-001,"the original text","why","ac",,C,'
        "Test,Approved\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / ".gitignore").write_text(
        "out/\nbar-cache/\n", encoding="utf-8", newline="\n"
    )
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n"
        "[generated]\nPROJECT_STATE.html = trajectory\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "review-policy").write_text("0\n", encoding="utf-8", newline="\n")
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(STUB_CHECK_GREEN, encoding="utf-8", newline="\n")
    _commit(root, "the attested spine + the stub harness", when=T_CODE)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    wt = close_branch(root, "wi-401")
    (wt / "docs" / "requirements" / "system-requirements.csv").write_text(
        sr_header + 'SR-001,Adder,SN-001,"the AMENDED text","why","ac",,C,'
        "Test,Approved\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(wt, "WI-401: amend the requirement without the flip", when=T_LATER)

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal is None, refusal

    minted = sorted((root / "docs" / "work" / "queued").glob("WI-402-*.md"))
    assert len(minted) == 1, minted
    text = minted[0].read_text(encoding="utf-8")
    assert 'safety_class = "adjudication"' in text
    assert "SR-001" in text and "## Context" in text
    assert "the original text" in text and "the AMENDED text" in text
    # The mint is its OWN bookkeeping commit, after the merge, on trunk.
    subjects = _git(root, "log", "--format=%s").splitlines()
    assert subjects[0].startswith("mint: WI-402"), subjects[:3]
    assert subjects[1].startswith("integrate: merge wi-401"), subjects[:3]


def test_the_bar_key_reaches_check_gate(tmp_path):
    # WI-388 (5): an optional frontmatter `bar = DevStg-Reqs|DevStg-Tests|DevStg-Impl`
    # pins the lane's verification strictness — the refresh passes it to check.py
    # as --stage (WI-498 slice 2 re-keyed the flag; the three VALUES are ladder
    # rungs and are unchanged), so a row claimed to deliver evidence at a level
    # still bars at that level if the derived value moves mid-flight. Asserted
    # off the recording stub's OWN argv.
    root = station_repo(tmp_path, bar="DevStg-Tests")
    wt = _lane(root, "wi-401")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    order = _order(wt)
    assert "--stage" in order and "DevStg-Tests" in order, order
    assert order.index("--stage") + 1 == order.index("DevStg-Tests")


def test_without_a_bar_key_the_refresh_passes_no_stage(tmp_path):
    # The complement, so the key cannot be mistaken for a default: an undeclared
    # bar leaves check.py on its own derived-stage read, exactly as before.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert "--stage" not in _order(wt)


def test_a_malformed_bar_value_refuses_the_refresh(tmp_path):
    # Fail closed and loud: a typo'd bar silently ignored would bar at whatever
    # docs/gate happens to read — the exact drift the key exists to pin. The
    # claimed spec lives on the branch, so the fix is a lane-side edit.
    root = station_repo(tmp_path, bar="G9")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "bar" in refusal and "G9" in refusal


def test_an_adjudication_lane_runs_no_bar(tmp_path):
    # WI-388 (1): adjudication runs NO BAR (§A5.2) — its outputs are Status
    # cells and the work registry, nothing a product bar can speak to. The
    # refresh still merges trunk in and runs the trunk step, still commits a
    # verified Bar-Green attestation (the slot's contract), but the check
    # harness is never invoked and the summary says so. `product=False`: the
    # lane's delta is the pure registry shape the kind's premise names — a
    # spine Status edit rides along and stays inside the scope rung.
    root = station_repo(tmp_path, safety="adjudication", product=False)
    wt = _lane(root, "wi-401")
    (wt / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (wt / "docs" / "requirements" / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        'SR-001,Adder,SN-001,"t","w","a",,C,Test,Approved\n',
        encoding="utf-8",
        newline="\n",
    )
    _commit(wt, "WI-401: the Status-cell judgement", when=T_LATER)
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert _order(wt) == ["trunk_step"], "the bar must not run for adjudication"
    attested = integ.refresh_attestation(root, "wi-401", sha)
    assert attested is not None
    assert "no-bar" in attested[1]
    ready, why = integ._merge_ready(root, "wi-401")
    assert ready and "no-bar" in why


def test_a_product_touching_adjudication_lane_fails_toward_the_bar(tmp_path):
    # REVIEW-A finding 1, the reviewer's own drive kept as the regression: a
    # product file plus a check harness that FAILS if invoked rode an
    # adjudication-only lane through the no-bar arm onto trunk — an un-run
    # green, against §A8's fixed points ("no un-run greens; the harness is
    # still the bar"). The scope rung closes it: the branch's non-refresh
    # delta touches a path outside the §A5.2 surfaces (the product file), so
    # the refresh runs the FULL bar — which is red, and says so.
    root = station_repo(tmp_path, check_src=STUB_CHECK_RED, safety="adjudication")
    wt = _lane(root, "wi-401")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "the bar is RED on the refreshed tree" in refusal
    assert "check-red" in _order(wt), "the harness must have RUN"
    ready, _why = integ._merge_ready(root, "wi-401")
    assert not ready


def test_a_mixed_claim_still_runs_the_bar(tmp_path):
    # Fail toward the bar: the no-bar arm arms only when EVERY claimed spec is
    # the adjudication kind. A batch claim holding one ordinary row beside the
    # adjudication row bars as usual.
    root = claim_repo(tmp_path, safety="adjudication")
    write_spec(root, "queued", "WI-402", slug="extra", specref="seed.txt")
    (root / ".gitignore").write_text(
        "out/\nbar-cache/\n", encoding="utf-8", newline="\n"
    )
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n", encoding="utf-8", newline="\n"
    )
    declare_generated(root)
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(STUB_CHECK_GREEN, encoding="utf-8", newline="\n")
    _commit(root, "chore: the stub harness and the declared bar", when=T_CODE)
    assert integ.claim(root, ["WI-401", "WI-402"], "wi-401") == 0
    wt, err = integ.lane_worktree(root, "wi-401")
    assert err is None, err
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert "check" in _order(wt)


# 5b.3 — the disposable-commit rule (§A2.1)


def test_a_second_refresh_replaces_the_first_and_never_stacks(tmp_path):
    # THE rule the determinism measurement forced. docs/log.md is APPEND-compiled
    # from docs/log.d/ fragments, so a second merge stacked on the first would
    # conflict on the file end — the exact failure §A2 exists to abolish. A retry
    # is therefore a reset to the last WORK commit and a fresh sequence: after
    # two refreshes the branch carries exactly ONE refresh commit, and its first
    # parent is still the work commit, not the previous refresh.
    root = station_repo(tmp_path)
    work_tip = _rev(root, "wi-401")
    first, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal

    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves, so the branch must refresh again", when=T_LATER)
    second, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal

    assert second != first
    assert _refresh_commits(root, "wi-401") == [second], "a refresh must not stack"
    assert _git(root, "rev-parse", second + "^1").strip() == work_tip
    assert integ._work_tip(root, "wi-401") == work_tip
    # The discarded first refresh is unreachable from the branch: nothing to
    # unpick, nothing to hand-merge.
    assert first not in _git(root, "rev-list", "wi-401").split()


def test_a_conflicting_trunk_merge_leaves_the_branch_at_its_work_commit(tmp_path):
    # The one place a conflict can still happen, and the lane owns it. What must
    # NOT happen is a parked half-merge: the branch is reset, the tree is clean,
    # MERGE_HEAD is gone, and the refusal says where to resolve it.
    root = station_repo(tmp_path)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    # Both sides edit the same line of the same file, from a common base.
    (wt / "contested.txt").write_text("branch side\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: the branch's take", when=T_VERDICT)
    (root / "contested.txt").write_text("trunk side\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: the trunk's take", when=T_LATER)
    work_tip = _rev(root, "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "CONFLICTS" in refusal and str(wt) in refusal
    assert _rev(root, "wi-401") == work_tip
    assert _git(wt, "status", "--porcelain").strip() == ""
    assert integ.ac.git(wt, "rev-parse", "--verify", "--quiet", "MERGE_HEAD")[0] != 0


def test_a_red_refresh_bar_commits_nothing_and_leaves_the_branch_clean(tmp_path):
    # A red bar is the lane's to fix, so the branch goes back to where the lane
    # left it — no refresh commit, no attestation, and therefore no way for the
    # slot to merge it. The bar really ran (the stub recorded itself) before the
    # tree was restored.
    root = station_repo(tmp_path, check_src=STUB_CHECK_RED)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    work_tip = _rev(root, "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "the bar is RED on the refreshed tree" in refusal
    assert "bar exit 1" in refusal
    assert _rev(root, "wi-401") == work_tip
    assert _refresh_commits(root, "wi-401") == []
    assert _git(wt, "status", "--porcelain").strip() == ""
    ready, _why = integ._merge_ready(root, "wi-401")
    assert not ready


def test_a_red_refusal_carries_the_steps_own_output_and_names_the_kept_log(tmp_path):
    # WI-398, driven end-to-end. Two halves of one loss: (1) the refusal's
    # bounded tail must be the failing STEP's own output — not check.py's
    # closing summary re-print, which is all the WI-240 anchor could ever reach
    # on a full bar; (2) the undo below resets the very tree that produced the
    # evidence, so the FULL bar output must survive OUTSIDE the lane worktree,
    # at a path the refusal message itself names. The WI-387 red cost three
    # lost diagnoses of one failure because neither half held.
    root = station_repo(tmp_path, check_src=STUB_CHECK_RED)
    wt = _lane(root, "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    # (1) the failing step's own output reached the refusal text ...
    assert "FAILED tests/test_widget.py::test_value" in refusal
    assert "  FAIL  tests+coverage" in refusal
    # ... and the summary re-print did not (the kept file holds it instead).
    assert "Check summary" not in refusal
    assert "RESULT: FAIL" not in refusal
    # (2) the message NAMES the retained full log, outside the lane worktree,
    # and the file really holds the WHOLE bar output — summary included.
    kept = root / "out" / "run-logs" / "refresh-refused-wi-401.log"
    assert str(kept) in refusal
    text = kept.read_text(encoding="utf-8")
    assert "FAILED tests/test_widget.py::test_value" in text
    assert "Check summary" in text and "RESULT: FAIL" in text
    # The evidence home survives the undo and leaves the lane clean: the next
    # refresh (or a hand rebuild) starts from the work tip, evidence in hand.
    assert _git(wt, "status", "--porcelain").strip() == ""
    assert _git(root, "status", "--porcelain").strip() == ""  # gitignored home


def test_the_refresh_refuses_rather_than_discard_uncommitted_lane_work(tmp_path):
    # The reset is what makes the retry safe, and it is also the one thing that
    # could destroy work. So the dirt check comes FIRST: a lane with uncommitted
    # changes is told to commit them, never reset over them.
    root = station_repo(tmp_path)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    (wt / "wi-401.txt").write_text("half-finished\n", encoding="utf-8", newline="\n")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "is dirty" in refusal and "commit or stash it" in refusal
    assert (wt / "wi-401.txt").read_text(encoding="utf-8") == "half-finished\n"


# 5b.4 — the two requirements the owner's caveat produced


def test_slot_acquisition_has_exactly_one_call_site():
    # §A2.0 requirement 1, and it is a claim ABOUT THE SOURCE, so it is checked
    # against the source. "Restricting the design to pessimistic is a one-line
    # change" is only true while every refresh that happens inside the slot
    # happens under a lock taken in one place; a second acquisition site would
    # make that a rewrite, quietly, and nothing else would notice.
    src = (SCRIPTS / "integrate.py").read_text(encoding="utf-8")
    sites = [ln for ln in src.splitlines() if "acquire_lock(" in ln]
    assert len(sites) == 1, sites
    assert "def _slot(root)" in src
    # ...and it is inside `_slot`, not merely singular.
    body = src.split("def _slot(root):", 1)[1].split("\ndef ", 1)[0]
    assert "acquire_lock(" in body
    # And the SLOT, not just the lock call: counting `acquire_lock(` alone let
    # a second acquisition through the existing helper pass (REVIEW-A round 1
    # drove it — `_extra = _slot(root)` at the top of `integrate_one` was
    # green). `_slot(` must occur exactly twice: the definition and its one
    # call, so a second acquisition by EITHER route reds here.
    calls = [ln for ln in src.splitlines() if "_slot(" in ln]
    assert len(calls) == 2, calls
    assert any(ln.strip().startswith("def _slot(") for ln in calls), calls


def test_the_pessimistic_sequence_runs_when_a_lane_loses_the_race(tmp_path):
    # §A2.0 requirement 2: the one-lost-race fallback IS the pessimistic
    # sequence, and it must not be dead code. It is not, by CONSTRUCTION — this
    # is a two-branch drain, and merging the first moves trunk out from under the
    # second, so the second loses the race every single time. Both branches
    # refresh themselves first (the speculative half, as drive.py does it); only
    # the loser is re-refreshed, in the slot.
    root = station_repo(tmp_path)
    write_spec(root, "queued", "WI-402", slug="gadget", order=1, specref="seed.txt")
    _commit(root, "file WI-402", when=T_CODE)
    assert integ.claim(root, "WI-402", "wi-402") == 0
    close_branch(root, "wi-402", wi="WI-402", slug="gadget")

    for branch in ("wi-401", "wi-402"):
        _sha, refusal = integ.refresh(root, branch, "smoke")
        assert refusal is None, refusal
    assert integ.trunk_is_ancestor(root, "wi-401")
    assert integ.trunk_is_ancestor(root, "wi-402")

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out

    # The winner merged on its speculative bar; the loser was named, refreshed
    # in the slot, and merged after — bar-time it would have paid anyway going
    # second, and nothing was reconciled because ancestry is all that moved.
    assert out.count("is not merge-ready") == 1, out
    assert "the pessimistic sequence" in out, out
    assert "wi-402 is not merge-ready" in out, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out
    assert "integrate: wi-402 merged (WI-402=merged)" in out, out
    # Both landed, and the second composed ON TOP of the first — the Class C
    # coverage the deleted composed-tree bar used to buy, now free.
    tracked = _git(root, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert "wi-401.txt" in tracked and "wi-402.txt" in tracked
    assert "wi-401" not in _branches(root) and "wi-402" not in _branches(root)


def test_a_branch_that_never_refreshed_is_refreshed_by_the_slot(tmp_path):
    # The degradation that makes the speculative half OPTIONAL: delete drive.py's
    # refresh call and the queue still works, one lane at a time, with the bar
    # inside the lock. That is the owner's caveat priced at one line — and it is
    # this path, so it is covered whether or not anyone ever exercises it.
    root = station_repo(tmp_path)
    assert integ.refresh_attestation(root, "wi-401") is None

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "not a verified refresh commit" in out, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out


def test_the_refresh_cli_is_the_lane_side_entry_point(tmp_path):
    # The seam drive.py and a worker share, exercised through the real CLI: one
    # operation, one branch, no slot taken. (`integrate` is the only operation
    # in this file that takes the slot — see the one-call-site test above.)
    root = station_repo(tmp_path)
    proc = run_py(
        [SCRIPTS / "integrate.py", "refresh", "--branch", "wi-401", "--tier", "smoke"],
        cwd=root,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "integrate: refreshed wi-401 onto trunk" in out, out
    assert integ.refresh_attestation(root, "wi-401")

    proc = run_py(
        [SCRIPTS / "integrate.py", "refresh", "--branch", "wi-999", "--tier", "smoke"],
        cwd=root,
    )
    assert proc.returncode != 0
    assert "cannot refresh wi-999" in proc.stdout + proc.stderr


# 5b.5 — the attestation is a BINDING, not a string (REVIEW-A round 1)
#
# Round 1 found the constraint's second half satisfiable by a message: any line
# starting with `Bar-Green:` made a branch merge-ready, so a forged trailer, a
# copied message and `commit --amend` all landed unbarred content on trunk, and
# the same unbound token drove a `reset --hard` that DELETED a work commit. Each
# of the four tests below is that exploit, kept as the regression.


FORGED_TRAILER = "Bar-Green: tree={t} work={w} bar PASS (2 steps, tier all)".format(
    t="0" * 40, w="1" * 40
)


def test_a_forged_bar_green_trailer_does_not_make_a_branch_merge_ready(tmp_path):
    # Exploit (a), three ways, because the fix has three independent checks and
    # a test that only drove one would let the other two rot. An ordinary
    # subject; the refresh SUBJECT with names that belong to nothing; and the
    # sharpest one — a genuine refresh commit's message COPIED verbatim onto a
    # different commit, which is what amend/rebase/cherry-pick do by accident.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")

    (wt / "sneaky.txt").write_text("unbarred\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: a perfectly ordinary work commit\n\n" + FORGED_TRAILER)
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why

    (wt / "sneaky.txt").write_text("still unbarred\n", encoding="utf-8", newline="\n")
    _commit(
        wt,
        "refresh: wi-401 onto trunk 0123456789\n\n" + FORGED_TRAILER,
        when=T_LATER,
    )
    assert integ.refresh_attestation(root, "wi-401") is None

    # Now a REAL refresh, then its whole message re-used on a new commit.
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    genuine = _git(root, "log", "-1", "--format=%B", "wi-401")
    assert integ.refresh_attestation(root, "wi-401") is not None
    (wt / "carried.txt").write_text("rode in\n", encoding="utf-8", newline="\n")
    _commit(wt, genuine, when=T_LATER)
    assert integ.refresh_attestation(root, "wi-401") is None, (
        "a copied refresh message names another commit's tree and parent"
    )
    ready, _why = integ._merge_ready(root, "wi-401")
    assert not ready


def test_the_queue_refuses_to_land_a_forged_attestation_unbarred(tmp_path):
    # The exploit end to end, which is what made it MAJOR: round 1's
    # `integrate --tier smoke` exited 0 and put `sneaky.txt` on trunk with the
    # recording stub harness never invoked at all. Now the slot does not
    # believe the trailer, falls into its pessimistic arm, and the file only
    # reaches trunk AFTER a real bar ran on it.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "sneaky.txt").write_text("unbarred\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: a perfectly ordinary work commit\n\n" + FORGED_TRAILER)
    assert _order(wt) == [], "no bar has run yet"

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "not a verified refresh commit" in out, out
    # The bar DID run this time — the forgery bought nothing but a refresh.
    assert "trunk_step" in _order(wt) and "check" in _order(wt), out
    assert "sneaky.txt" in _git(root, "ls-tree", "-r", "--name-only", "HEAD")


def test_amending_a_refresh_commit_revokes_its_attestation(tmp_path):
    # Exploit (b): `commit --amend --no-edit` keeps the message while the tree
    # moves, so round 1 landed the amended-in file with the bar not re-run. The
    # trailer names the tree, so an amend that changes content cannot keep it.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    before = _git(root, "rev-parse", "wi-401^{tree}").strip()
    runs = len(_order(wt))

    (wt / "amended-in.txt").write_text("unbarred\n", encoding="utf-8", newline="\n")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "--amend", "--no-edit")
    assert _git(root, "rev-parse", "wi-401^{tree}").strip() != before

    assert integ.refresh_attestation(root, "wi-401") is None
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why
    # And end to end: the amended content still reaches trunk, but only through
    # a fresh bar — which is the correct outcome, not a refusal.
    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert len(_order(wt)) > runs, "the amended tree was barred before it merged"
    assert "amended-in.txt" in _git(root, "ls-tree", "-r", "--name-only", "HEAD")


def test_a_work_commit_that_quotes_the_trailer_is_never_peeled_away(tmp_path):
    # The data-loss half. `_work_tip` feeds a `reset --hard`, so peeling one
    # commit too far DESTROYS committed work: in round 1 a commit carrying
    # `Bar-Green: I ran it locally, honest` was peeled and its file left the
    # branch entirely. The peel now needs a commit that names its own tree and
    # parent, which no hand-written message can do by accident.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "late.txt").write_text("real work\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: late fix\n\nBar-Green: I ran it locally, honest", when=T_LATER)
    tip = _rev(root, "wi-401")

    assert integ._work_tip(root, "wi-401") == tip, "an honest tip must not peel"
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    tracked = _git(root, "ls-tree", "-r", "--name-only", "wi-401").split()
    assert "late.txt" in tracked, tracked
    # ...and the genuine refresh on top of it still peels back to exactly it.
    assert integ._work_tip(root, "wi-401") == tip


def test_the_refresh_sheds_its_residue_inside_a_directory_that_predates_it(tmp_path):
    # Round 1: `git status --ignored=matching` collapses an ignored directory to
    # ONE line at any -u setting, so a before/after line diff skipped the whole
    # directory when it already existed — and that is the NORMAL case, since the
    # worker builds in the same lane worktree the refresh then bars. Driven with
    # the directory pre-created, which the previous listing could not see into.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "bar-cache").mkdir()
    (wt / "bar-cache" / "worker-run.txt").write_text(
        "the worker's, not ours\n", encoding="utf-8", newline="\n"
    )
    assert integ._worktree_dirt(wt) == ["!! bar-cache/"], "the collapsed listing"

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert not (wt / "bar-cache" / "run.txt").exists(), "the refresh's own file"
    assert (wt / "bar-cache" / "worker-run.txt").is_file(), "the lane's own file"
    # The directory SURVIVES, because it still holds a file that predates the
    # refresh — and §5.6 will therefore still report this lane as dirty. That is
    # WI-359's rule working, and the refresh's promise is only that it added
    # nothing to the pile.
    assert (wt / "bar-cache").is_dir()


def test_an_empty_directory_that_predates_the_refresh_is_not_pruned(tmp_path):
    # REVIEW-A round 2. The prune has to exist — git DOES report an emptied
    # ignored directory (`!! bar-cache/`), so leaving one would make §5.6's
    # unload refuse over a directory the refresh had just emptied. But it
    # reached one step too far: an EMPTY directory that predates the refresh is
    # the lane's, and emptiness can be load-bearing — this repo's own
    # `docs/work/deferred/` is an empty untracked directory a link resolves
    # through. Driven with the directory pre-created and empty, which no git
    # listing can distinguish from one the bar made.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "bar-cache").mkdir()  # pre-existing, EMPTY, ignored
    assert integ.ignored_files(wt) == set(), "git lists no file for an empty dir"

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert not (wt / "bar-cache" / "run.txt").exists(), "the bar's file is shed"
    assert (wt / "bar-cache").is_dir(), "the lane's empty directory survives"


def test_a_directory_the_bar_itself_created_is_pruned(tmp_path):
    # The other answer, so the guard above is a rule with two outcomes rather
    # than a prune that never fires. Nothing pre-exists here, so `bar-cache/`
    # is the refresh's own and goes — otherwise git reports the emptied
    # directory and the merge exits nonzero over the integrator's own leavings.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    assert not (wt / "bar-cache").exists()

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert not (wt / "bar-cache").exists(), "the refresh's own directory is shed"
    assert integ._worktree_dirt(wt) == [], "...so the lane reads clean to §5.6"


def test_a_deliberately_forged_attestation_is_a_STATED_limit_not_a_defence(tmp_path):
    # The honest bound, pinned so nobody re-reads the guarantee as stronger than
    # it is (REVIEW-A round 2 drove it). Naming the tree and the parent by hand
    # is four git invocations and no bar, and it VERIFIES — this test asserts the
    # limit rather than a defence, because the only structural closure is a
    # slot-side re-bar and DECISION 3 (owner ruling) deleted that outright.
    # If this test ever starts failing, the design changed: re-read §A2.0 and
    # `refresh_attestation`'s contract before "fixing" it.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "never-barred.txt").write_text("no bar\n", encoding="utf-8", newline="\n")
    _git(wt, "add", "-A")
    tree = _git(wt, "write-tree").strip()
    parent = _rev(root, "wi-401")
    _git(
        wt,
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-qm",
        "refresh: wi-401 onto trunk deadbeef01\n\n"
        "Bar-Green: tree={} work={} bar PASS (99 steps, tier all)".format(tree, parent),
    )

    assert integ.refresh_attestation(root, "wi-401") == (
        parent,
        "bar PASS (99 steps, tier all)",
    )
    ready, _why = integ._merge_ready(root, "wi-401")
    assert ready, "accepted BY DESIGN - the bound is accident, not intent"
    assert _order(wt) == [], "and no bar ever ran"


def test_a_cancelled_branch_merges_through_the_slot_owing_no_verdict(tmp_path):
    # The outcome keying, driven through the WHOLE slot rather than at the gate
    # helper: review-policy 1, no verdict artifact anywhere, and a lane whose
    # specs went to `cancelled/`. It merges — because the cancellation is a
    # trunk fact and the id stays retired, which is only true if the branch
    # lands. (`test_only_the_merged_outcome_owes_a_verdict` shows the same repo
    # shape refusing when the outcome is `merged`, so this is not vacuous.)
    root = station_repo(tmp_path, policy="1", dest="cancelled")

    assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": "cancelled"}, [])
    assert integ.integrate(root, "smoke") == 0
    assert (root / "docs" / "work" / "cancelled" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_the_refresh_refuses_when_the_main_checkout_holds_the_branch(tmp_path):
    # Round 1: with the main checkout on the branch, `_head(root)` IS the branch,
    # so the refresh "merged trunk in" from itself, printed a trunk sha that was
    # the branch's own, and attested a composition that never happened. There is
    # no trunk to resolve while nothing has it checked out, so it refuses.
    root = station_repo(tmp_path)
    _git(root, "worktree", "remove", str(_lane(root, "wi-401")))
    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves", when=T_LATER)
    _git(root, "checkout", "-q", "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "MAIN checkout" in refusal and "no trunk checked out" in refusal
    assert "checkout <trunk>" in refusal
    assert integ.refresh_attestation(root, "wi-401") is None
    assert not (root / "trunk-moved.txt").exists(), "nothing was merged in"


# 5b.6 — the refresh must not stale an honest verdict


def test_the_mechanical_refresh_does_not_stale_a_good_verdict(tmp_path):
    # A structural consequence of moving the bar onto the branch: the refresh is
    # the LAST commit before the merge, and it lands after the review by
    # construction. If it counted as "code", the RULING-7 freshness rule would
    # be unpassable for every WI. The refresh is peeled off (`_work_tip`) — and
    # the neighbouring stale-APPROVE tests are what prove this is an exclusion
    # rather than a broken comparison.
    root = station_repo(tmp_path)
    (root / "docs" / "review-policy").write_text("1\n", encoding="utf-8", newline="\n")
    _commit(root, "policy: require a verdict", when=T_CODE)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    verdict = wt / "docs" / "reviews" / "WI-401-REVIEW-A.md"
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text(VERDICT_APPROVE, encoding="utf-8", newline="\n")
    _commit(wt, "review: WI-401 REVIEW-A", when=T_LATER)
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_claim_build_and_integrate_end_to_end(tmp_path):
    """The whole flow as a user runs it: scaffold -> claim -> build on the
    branch -> close -> `integrate --tier smoke`, against the REAL bar
    (`scaffolded_closed_branch` documents the fixture)."""
    repo, claim_sha = scaffolded_closed_branch(tmp_path)

    # 3. the queue.
    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out

    # The bar really ran: a step count, at the tier asked for, with no SKIP.
    bar = re.search(r"bar PASS \((\d+) steps, tier smoke\)", out)
    assert bar, out
    assert int(bar.group(1)) >= 10, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out
    assert "integrate: audit clean" in out, out

    # This branch never refreshed (nothing called it), so the slot said so and
    # ran the PESSIMISTIC sequence itself. That arm is on the ordinary path,
    # not an exotic one — which is exactly why it cannot rot (§A2.0).
    assert "is not merge-ready" in out, out
    assert "the pessimistic sequence" in out, out
    assert "integrate: refreshed wi-401 onto trunk" in out, out

    # The trunk advanced to a --no-ff MERGE of the branch onto the claim commit.
    parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").split()
    assert len(parents) == 3, parents
    assert parents[1] == claim_sha
    assert (
        _git(repo, "log", "-1", "--format=%s")
        .strip()
        .startswith("integrate: merge wi-401")
    )
    # ...and the merge's tree IS the branch tip's, byte for byte. That identity
    # is the whole reason the merge bar could be deleted: there is no composed
    # tree left to check, because the composition already happened at refresh.
    assert _git(repo, "rev-parse", "HEAD^{tree}") == _git(
        repo, "rev-parse", parents[2] + "^{tree}"
    )

    # The claim is released: the branch is gone and active/<branch>/ is empty in
    # the trunk's tree, with the spec closed by the branch's own closing move.
    assert "wi-401" not in _branches(repo)
    tracked = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert not [p for p in tracked if p.startswith("docs/work/active/wi-401/")], tracked
    assert "docs/archive/work/complete/WI-401-widget.md" in tracked
    # No integrator-owned worktree exists to tear down any more: the trunk is
    # the only registration left, and the lane the refresh used was GC'd by the
    # §5.6 unload rather than by a teardown of its own. (Trunk's side of this
    # merge asserted `CANDIDATE_BRANCH` was cleaned up; that constant and the
    # worktree it named are what this WI deleted, so the assertion is not
    # dropped to settle a conflict - it has no subject left.)
    assert not (tmp_path / "repo-integrate").exists()
    assert _worktree_count(repo) == 1
    assert _git(repo, "status", "--porcelain").strip() == ""


def test_integrate_is_a_noop_when_no_claimed_branch_has_finished(tmp_path):
    # The quiet steady state — the queue runs on a schedule, so "nothing to
    # merge" must be a cheap green, never a nonzero that would halt claiming.
    # Run as a SUBPROCESS: integrate() takes the process-global lock fd.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "chore: ignore the coordinator lock", when=T_VERDICT)

    proc = run_py([SCRIPTS / "integrate.py", "integrate"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "no finished claimed branches" in out, out


def test_integrate_refuses_and_holds_the_trunk_when_the_bar_is_undeclared(tmp_path):
    # The §4 refusal reached through the real CLI, on a finished branch: the
    # queue would otherwise be free to merge, and a repo with no declared bar is
    # precisely where a fail-open merge does its damage. The trunk must not move.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    # The fixture declares `[generated]` (see `declare_generated`), which is a
    # stack.ini — and THIS test is about the file being ABSENT, which is a
    # distinct §4 refusal from a stack.ini that declares no [product] test. So
    # it is removed here, after the claim that needed it, rather than the
    # assertion being softened to whichever refusal happens to fire.
    (root / "docs" / "stack.ini").unlink()
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "chore: ignore the coordinator lock", when=T_VERDICT)
    trunk_before = _rev(root, "HEAD")

    _git(root, "checkout", "-q", "wi-401")
    (root / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/complete/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> complete", when=T_LATER)
    _git(root, "checkout", "-q", "main")

    proc = run_py([SCRIPTS / "integrate.py", "integrate"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "docs/stack.ini is absent" in out, out
    assert _rev(root, "HEAD") == trunk_before
    assert "wi-401" in _branches(root)


# --- the bar step count is honest (WI-377) ------------------------------------


def test_bar_step_count_is_by_distinct_name_not_by_echoed_line():
    # Under --jobs each step's status line prints TWICE (the lane runner as it
    # finishes, then the final summary block), so a line count reported a
    # 20-step bar as ""bar PASS (40 steps)"" - a false measurement in the
    # merge record (WI-377). The count is by DISTINCT step name, so the
    # --jobs N output (doubled lines) and the --jobs 1 output (single lines)
    # of the same plan report the SAME step count.
    lane_echo = (
        "  PASS  format           0.1s\n"
        "  PASS  lint             0.2s\n"
        "  PASS  tests+coverage   61.0s\n"
    )
    summary = (
        "=" * 56 + "\n"
        "  PASS  format           0.1s\n"
        "  PASS  lint             0.2s\n"
        "  PASS  tests+coverage   61.0s\n"
    )
    jobs_n = lane_echo + summary  # every line twice, the --jobs shape
    jobs_1 = summary  # the serial shape
    assert integ._passed_steps(jobs_n) == integ._passed_steps(jobs_1)
    assert len(integ._passed_steps(jobs_n)) == 3
    # A FAIL/SKIP line never counts as a pass, and a malformed PASS line
    # (no name field) cannot crash the read.
    mixed = jobs_n + "  FAIL  dupes  exit 1 (0.1s)\n  SKIP  okf  absent\nPASS\n"
    assert len(integ._passed_steps(mixed)) == 3
