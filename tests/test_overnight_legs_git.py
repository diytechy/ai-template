"""The overnight-leg launcher on a real git repository with stub legs
(`scripts/coordinator/overnight_legs.py`, this repository's own tooling).

Each case builds a repository holding one handoff, puts a stub `claude` on a
PATH that holds only it and git (`overnight_legs_fixtures.stub_claude`), and
runs the launcher's `main()` in process for two legs. Every stub leg records
the marker and the prompt it got; finding no marker it writes nothing, as the
headless block tells a real leg, and otherwise it commits the next handoff
with the run's trailer. Its in-process pin is `test_overnight_legs`.
"""

import sys

import agent_brief
import agent_common
import coordinator_guard
import pytest
from kitlib import provenance

from overnight_legs_fixtures import (
    BLOCK,
    LOOP_SESSION_ENV,
    OTHER_SESSION,
    handoff_repo,
    lane_commit,
    lane_setup,
    leg_records,
    load_launcher,
    stub_claude,
)

WELL_FORMED = "20260101T000000Z-abcdef"


@pytest.fixture
def ol(tmp_path, monkeypatch):
    """The launcher, logging under `tmp_path`, with `sys.path` restored."""
    monkeypatch.setattr(sys, "path", list(sys.path))
    module = load_launcher()
    monkeypatch.setattr(module, "LOGDIR", tmp_path / "logs")
    monkeypatch.setattr(module, "lease_holder", lambda repo: None)
    return module


def run_two_legs(ol, tmp_path, monkeypatch, plan=None, setup=None):
    """Run two legs over a fresh repository, each performing its entry of
    `plan` (default: a marked handoff), after `setup(repo)` when given;
    return (exit, records, repo)."""
    repo = handoff_repo(tmp_path / "repo")
    if setup:
        setup(repo)
    records = stub_claude(tmp_path, monkeypatch, plan)
    code = ol.main(["--repo", str(repo), "--max-legs", "2"])
    return code, leg_records(records), repo


def run_log(ol):
    return (ol.LOGDIR / "loop.log").read_text(encoding="utf-8")


def check_lane(ol, repo, capsys):
    """`check-lane wi-1`'s exit code and output; argparse's own exit counts."""
    try:
        code = ol.main(["check-lane", "wi-1", "--repo", str(repo)])
    except SystemExit as exc:
        code = exc.code
    return code, capsys.readouterr().out


def marked_lane(repo):
    """A lane `wi-1` with a marked claim, holding a marked commit, an
    unmarked one (`lane work 2`) and a marked one."""
    lane_setup(repo, WELL_FORMED, [WELL_FORMED, None, WELL_FORMED])


def well_formed(session):
    return (
        bool(session)
        and provenance.mark_loop_process({LOOP_SESSION_ENV: session}) == session
    )


def test_two_legs_see_one_well_formed_marker_the_same_in_both(
    ol, tmp_path, monkeypatch
):
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch)
    assert code == 0
    assert len(records) == 2
    assert well_formed(records[0]["marker"])
    assert records[0]["marker"] == records[1]["marker"]


@pytest.mark.parametrize("inherited", [WELL_FORMED, "not a session!"])
def test_an_inherited_well_formed_marker_is_kept_and_a_malformed_one_is_replaced(
    ol, tmp_path, monkeypatch, inherited
):
    monkeypatch.setenv(LOOP_SESSION_ENV, inherited)
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch)
    assert code == 0 and len(records) == 2
    session = records[0]["marker"]
    assert well_formed(session)
    assert (session == inherited) == (inherited == WELL_FORMED)
    trailer = "`{}`".format(provenance.format_loop_trailer(session))
    for record in records:
        assert record["marker"] == session
        assert trailer in record["prompt"].splitlines()[-1]


def test_each_leg_gets_the_session_prompt_then_the_block_then_the_provenance_line(
    ol, tmp_path, monkeypatch
):
    code, records, repo = run_two_legs(ol, tmp_path, monkeypatch)
    assert code == 0 and len(records) == 2
    block = BLOCK.read_text(encoding="utf-8").strip()
    assert 'echo "$KIT_LOOP_SESSION"' in block.splitlines()[0]
    monkeypatch.setenv(LOOP_SESSION_ENV, records[0]["marker"])
    note = agent_brief.loop_provenance_note()
    for leg, record in enumerate(records, start=1):
        handoff = repo / "docs" / "handoff-{:03d}.md".format(leg)
        expected = coordinator_guard.session_prompt(handoff) + "\n\n" + block + note
        assert record["prompt"] == expected


def head(repo):
    from integrate_fixtures import _git

    return _git(repo, "rev-parse", "HEAD").strip()


@pytest.mark.parametrize(
    "plan, named",
    [
        (["trunk_unmarked", "handoff"], "unmarked trunk work"),
        (["trunk_foreign", "handoff"], "foreign trunk work"),
        # A pin for the archive: one the leg creates is judged over the
        # commits no pre-leg branch reaches, as before.
        (["archive_unmarked", "handoff"], "unmarked archive record"),
        (["rewind", "handoff"], "pre-leg tip"),
    ],
    ids=["unmarked", "foreign", "archive", "rewind"],
)
def test_a_leg_that_adds_an_unmarked_foreign_or_rewinding_trunk_or_archive_commit_stops_the_run(
    ol, tmp_path, monkeypatch, plan, named
):
    tips = []
    code, records, _repo = run_two_legs(
        ol, tmp_path, monkeypatch, [plan], setup=lambda repo: tips.append(head(repo))
    )
    assert code == 3 and len(records) == 1
    stop = [line for line in run_log(ol).splitlines() if "stop:" in line][-1]
    assert named in stop
    if named == "pre-leg tip":
        assert tips[0][:10] in stop


def claimed_unmarked(repo):
    """A lane claimed without the trailer before the run, holding a person's
    commit."""
    lane_setup(repo, None, [None])


@pytest.mark.parametrize("follow_up", ["lane_marked", "squash_marked"])
@pytest.mark.parametrize(
    "mark, setup",
    [("claim_marked", None), ("telemetry_marked", claimed_unmarked)],
    ids=["marked-claim", "telemetry"],
)
def test_a_leg_that_adds_an_unmarked_commit_to_a_lane_it_marked_stops_the_run_naming_it(
    ol, tmp_path, monkeypatch, mark, setup, follow_up
):
    plan = [[mark, "lane_unmarked", follow_up, "handoff"]]
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch, plan, setup)
    assert code == 3 and len(records) == 1
    stop = [line for line in run_log(ol).splitlines() if "stop:" in line][-1]
    assert "unmarked lane work" in stop and "wi-1" in stop


def test_check_lane_refuses_a_marked_lane_holding_an_unmarked_commit_before_the_squash(
    ol, tmp_path, capsys
):
    repo = handoff_repo(tmp_path / "repo")
    marked_lane(repo)
    code, out = check_lane(ol, repo, capsys)
    assert code == 3
    assert "lane work 2" in out


@pytest.mark.parametrize(
    "order, code",
    [(("reclaim", "work"), 0), (("work", "reclaim"), 3)],
    ids=["after-the-reclaim", "before-the-reclaim"],
)
def test_check_lane_reads_a_reclaim_as_the_merge_slot_does(
    ol, tmp_path, capsys, order, code
):
    # A lane claimed under the marker, then the attended re-claim (an empty,
    # unmarked commit under the lane's re-claim subject) and an unmarked
    # commit: after the re-claim the commit is exempt, before it the commit is
    # refused by name, and the merge slot's trailer rung agrees on the same
    # repository.
    from integrate_fixtures import integ

    repo = handoff_repo(tmp_path / "repo")
    lane_setup(repo, WELL_FORMED, [WELL_FORMED])
    messages = {
        "reclaim": provenance.reclaim_subject("wi-1"),
        "work": "lane work 2",
    }
    for step in order:
        lane_commit(repo, messages[step])
    got, out = check_lane(ol, repo, capsys)
    slot = integ._loop_trailer_refusal(repo, "wi-1")
    assert got == code, out
    if code:
        assert "lane work 2" in out and slot and "lane work 2" in slot, slot
    else:
        assert slot is None


@pytest.mark.parametrize(
    "claim, commits",
    [(OTHER_SESSION, [OTHER_SESSION, OTHER_SESSION]), (None, [None, None])],
    ids=["another-run", "a-persons-lane"],
)
def test_a_lane_whose_replayed_commits_carry_another_runs_session_passes(
    ol, tmp_path, monkeypatch, capsys, claim, commits
):
    code, records, repo = run_two_legs(
        ol,
        tmp_path,
        monkeypatch,
        [["handoff", "replay_lane"]],
        setup=lambda repo: lane_setup(repo, claim, commits),
    )
    assert code == 0 and len(records) == 2
    assert check_lane(ol, repo, capsys)[0] == 0


def test_a_git_read_that_fails_after_a_leg_stops_the_run_and_check_lane_refuses(
    ol, tmp_path, monkeypatch, capsys
):
    plan = [
        ["claim_marked", "lane_marked", "lane_marked", "drop_lane_parent", "handoff"]
    ]
    code, records, repo = run_two_legs(ol, tmp_path, monkeypatch, plan)
    assert code == 3 and len(records) == 1
    stop = [line for line in run_log(ol).splitlines() if "stop:" in line][-1]
    assert "refs/heads/wi-1" in stop and "failed" in stop
    assert check_lane(ol, repo, capsys)[0] == 3


def test_a_leg_whose_commits_all_carry_the_runs_trailer_runs_the_next_leg(
    ol, tmp_path, monkeypatch
):
    # A pin for the archive too: a marked archive the leg creates passes.
    plan = [["claim_marked", "lane_marked", "lane_marked", "archive_marked", "handoff"]]
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch, plan)
    assert code == 0 and len(records) == 2
    assert "wi-1" in run_log(ol)


# --- the trunk the run binds, and the checkout held to it ----------------------


def stops(ol):
    return [line for line in run_log(ol).splitlines() if "stop:" in line]


def test_a_leg_that_leaves_the_primary_checkout_off_trunk_stops_the_run(
    ol, tmp_path, monkeypatch
):
    plan = [["checkout_elsewhere", "handoff"], ["main_unmarked", "handoff"]]
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch, plan)
    assert code == 3 and len(records) == 1
    assert "elsewhere" in stops(ol)[-1]


def test_the_run_binds_trunk_once_and_logs_it(ol, tmp_path, monkeypatch):
    calls = []
    real = agent_common.trunk_name

    def counted(repo, *args, **kwargs):
        calls.append(repo)
        return real(repo, *args, **kwargs)

    monkeypatch.setattr(agent_common, "trunk_name", counted)
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch)
    assert code == 0 and len(records) == 2
    assert len(calls) == 1
    assert "run trunk main" in run_log(ol)
    assert not hasattr(ol, "trunk_name")


def test_a_refusing_trunk_reader_stops_the_run_before_any_leg(
    ol, tmp_path, monkeypatch
):
    def refusing(repo, *args, **kwargs):
        raise ValueError("trunk undeclared: probe")

    monkeypatch.setattr(agent_common, "trunk_name", refusing)
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch)
    assert code == 2 and records == []
    assert "trunk undeclared: probe" in stops(ol)[-1]


def test_a_bound_name_no_local_branch_holds_stops_before_the_leg(
    ol, tmp_path, monkeypatch
):
    # A pin: the kit reader's last resort, "HEAD", names no local branch, and
    # the run stops before the leg, as a detached checkout stopped it before.
    monkeypatch.setattr(agent_common, "trunk_name", lambda repo, *a, **k: "HEAD")
    code, records, _repo = run_two_legs(ol, tmp_path, monkeypatch)
    assert code == 3 and records == []
    assert "refs/heads/HEAD" in stops(ol)[-1]


def archive_two(repo):
    """Two `archive/lanes` commits on trunk's tip, written before the run."""
    from integrate_fixtures import _git

    parent = head(repo)
    for n in (1, 2):
        message = "archive record {}".format(n)
        sha = _git(repo, "commit-tree", parent + "^{tree}", "-p", parent, "-m", message)
        parent = sha.strip()
    _git(repo, "update-ref", "refs/heads/archive/lanes", parent)


def archive_tip(repo):
    from integrate_fixtures import _git

    return _git(repo, "rev-parse", "refs/heads/archive/lanes").strip()


@pytest.mark.parametrize(
    "action", ["archive_rewind", "archive_reset_unrelated", "archive_delete"]
)
def test_a_leg_that_rewinds_resets_or_deletes_archive_lanes_stops_the_run(
    ol, tmp_path, monkeypatch, action
):
    tips = []

    def setup(repo):
        archive_two(repo)
        tips.append(archive_tip(repo))

    code, records, _repo = run_two_legs(
        ol, tmp_path, monkeypatch, [[action, "handoff"]], setup=setup
    )
    assert code == 3 and len(records) == 1
    assert tips[0][:10] in stops(ol)[-1]


def test_a_marked_archive_commit_on_an_existing_archive_runs_the_next_leg(
    ol, tmp_path, monkeypatch
):
    # A pin: an archive that descends, by a marked commit, passes.
    plan = [["archive_marked", "handoff"]]
    code, records, _repo = run_two_legs(
        ol, tmp_path, monkeypatch, plan, setup=archive_two
    )
    assert code == 0 and len(records) == 2
    assert "archive/lanes 1 commit(s)" in run_log(ol)


def test_check_lane_from_the_lanes_own_worktree_judges_from_the_kits_trunk(
    ol, tmp_path, capsys
):
    from integrate_fixtures import _git

    repo = handoff_repo(tmp_path / "repo")
    marked_lane(repo)
    lane = tmp_path / "lane"
    _git(repo, "worktree", "add", "-q", str(lane), "wi-1")
    code, out = check_lane(ol, lane, capsys)
    assert code == 3
    assert "lane work 2" in out


def test_the_leg_log_line_names_the_bound_trunks_pre_and_post_leg_tips(
    ol, tmp_path, monkeypatch
):
    # A pin on real git: the checkout stays on trunk here, so the line read
    # the same tips before the change.
    from integrate_fixtures import _git

    tips = []
    code, records, repo = run_two_legs(
        ol, tmp_path, monkeypatch, setup=lambda repo: tips.append(head(repo))
    )
    assert code == 0 and len(records) == 2
    after = _git(
        repo, "log", "--format=%H", "--fixed-strings", "--grep=handoff: leg 1", "main"
    ).split()
    assert len(after) == 1
    line = "leg 1 exit 0; trunk {} -> {}".format(tips[0][:8], after[0][:8])
    assert line in run_log(ol)
