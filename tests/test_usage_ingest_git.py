"""The usage ingest (`usage_ingest.py`) on real repositories: a claimed lane
(`conftest.claimed_lane`, a primary checkout and a linked worktree whose
claim is committed), a log held in another worktree, and the primary
checkout. The command runs in process; git is spawned for every lane read
and record commit. Its in-process pin is `test_usage_ingest.py`.

The Claude home is a tmp copy of the cut fixtures
(`claude_transcript_fixtures`).
"""

import types
from pathlib import Path

import pytest
from conftest import claimed_lane, fixture_commit, fixture_git, load_script

import claude_transcript_fixtures as fx
import codex_call_fixtures as cfx

ui = load_script("usage_ingest")
ac = load_script("agent_common")
brief = load_script("agent_brief")
cc = cfx.load_codex_call()

from kitlib import verdict as kv  # noqa: E402  (scripts/ is on sys.path now)


ITER = "docs/iteration"


@pytest.fixture
def home(tmp_path, monkeypatch):
    home = fx.home_copy(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home))
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    return home


def _lane(tmp_path):
    return claimed_lane(tmp_path / "repo", files={".gitignore": "out/\n"})


def _primary(lane):
    return lane.with_name(lane.name[: -len("-lane")])


def _ingest(root):
    return ui.main(["--session", fx.NESTED, "--root", str(root)])


def _tracked_call_logs(root):
    listed = fixture_git(root, "ls-files", "--", ITER)
    return sorted(p for p in listed.splitlines() if "/call_" in p)


def _state(root):
    return (
        fixture_git(root, "for-each-ref", "--format=%(refname) %(objectname)"),
        fixture_git(root, "rev-parse", "HEAD"),
        fixture_git(root, "status", "--porcelain", "--untracked-files=all"),
    )


def _build_log(iter_dir):
    """A gate log of a BUILD session, its name sorting before every `call_`
    name, so a reverse name walk reaches it last."""
    meta = {
        "session": "001",
        "stamp": "20200101-000000",
        "phase": "BUILD",
        "model": "m-build",
        "outcome": "COMMITTED",
    }
    return ac.write_session_log(iter_dir, meta, "")


def _round(lane, base):
    """One review round in the lane, in the loop's two steps: the verdict
    file named for the reviewed head, then the session log recording that
    session's commit range and its full scope from `base`."""
    before = fixture_git(lane, "rev-parse", "HEAD")
    rnd = lane / "docs" / "reviews" / "wi-1" / "001-REVIEW-A-{}.md".format(before[:7])
    rnd.parent.mkdir(parents=True, exist_ok=True)
    rnd.write_text(
        "Reviewed: {}\n\n# Review A\n\nVERDICT: APPROVE findings=0\n".format(before),
        encoding="utf-8",
        newline="\n",
    )
    fixture_commit(lane, "review: round 1")
    return before, fixture_git(lane, "rev-parse", "HEAD")


def _gate_log(lane, base, before, after):
    log = lane / ITER / "wi-1-001-20200101-000001.log"
    log.write_text(
        "# agent-loop session log\n# session: 001\n# train: wi-1\n"
        "# phase: REVIEW-A\n# outcome: COMMITTED\n"
        "# commits: {}..{}\n# review-scope: full {}..{}\n# session-gen: \n".format(
            before, after, base, before
        ),
        encoding="utf-8",
        newline="\n",
    )
    fixture_commit(lane, "telemetry: session wi-1-001")


def _rounds(lane, base):
    paths = fixture_git(lane, "diff", "--name-only", base, "HEAD").splitlines()
    return kv.logged_rounds(lane, "wi-1", base, paths)


def test_an_ingested_log_in_a_lane_is_no_round_no_build_and_no_draw(tmp_path, home):
    lane = _lane(tmp_path)
    base = fixture_git(lane, "rev-parse", "HEAD")
    iter_dir = lane / ITER
    author = cfx.call_log(iter_dir, stamp="20200101-000000", session_id="T-OLD")
    _build_log(iter_dir)
    fixture_commit(lane, "the lane's AUTHOR and BUILD logs")
    draws = ac.phase_draw_ordinal([iter_dir], "BUILD")
    assert draws == 1
    assert _ingest(lane) == 0
    ingested = [p for p in _tracked_call_logs(lane) if not p.endswith(author.name)]
    assert len(ingested) == 4
    assert fixture_git(lane, "status", "--porcelain") == ""

    # a round file with no gate log of its own is no round, though four
    # ingested logs sit beside it; with its gate log it is one
    before, after = _round(lane, base)
    assert _rounds(lane, base) == []
    _gate_log(lane, base, before, after)
    assert [r[:3] for r in _rounds(lane, base)] == [(1, "REVIEW-A", before[:7])]

    # the build family is the BUILD log's, though the reverse name walk meets
    # the ingested logs first and the registry knows their model too
    registry = {
        "B": types.SimpleNamespace(id="B", model="m-build", family="fam-build"),
        "I": types.SimpleNamespace(
            id="I", model="claude-opus-5-5", family="fam-ingested"
        ),
    }
    assert brief.last_build_family(iter_dir, registry) == "fam-build"

    # no draw: neither role advances a rotation, and BUILD's count is as it was
    assert ac.phase_draw_ordinal([iter_dir], "SUBAGENT") == 0
    assert ac.phase_draw_ordinal([iter_dir], "COORDINATOR") == 0
    assert ac.phase_draw_ordinal([iter_dir], "BUILD") == draws

    # the resume carrier is the AUTHOR log, though every ingested log's stamp
    # is newer than its
    carrier = cc.read_carrier(lane, "OPENAI-TERRA")
    assert carrier.refusal == ""
    assert carrier.session_id == "T-OLD"


def test_a_log_in_another_worktree_counts_toward_exactly_once(tmp_path, home, capsys):
    lane = _lane(tmp_path)
    assert _ingest(lane) == 0
    assert len(_tracked_call_logs(lane)) == 4
    primary = _primary(lane)
    capsys.readouterr()
    assert _ingest(primary) == 0
    out = capsys.readouterr().out
    assert len([line for line in out.splitlines() if "unchanged" in line]) == 4
    spool = ui.session_service.spool_dir(primary)
    assert sorted(spool.glob("call_*.log")) == []


def test_from_the_primary_checkout_the_logs_spool_and_nothing_is_committed(
    tmp_path, home
):
    primary = _primary(_lane(tmp_path))
    before = _state(primary)
    assert _ingest(primary) == 0
    spool = ui.session_service.spool_dir(primary)
    assert len(sorted(spool.glob("call_*.log"))) == 4
    assert _state(primary) == before
    assert _tracked_call_logs(primary) == []


def test_a_refused_record_commit_exits_one_and_names_the_refusal(
    tmp_path, home, capsys
):
    # The lane's pre-commit hook vetoes every commit. Adequacy witness: a
    # command that read a refused commit as recorded would exit 0, and one
    # that hid it would print `committed`.
    lane = _lane(tmp_path)
    hook = Path(fixture_git(lane, "config", "core.hooksPath")) / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8", newline="\n")
    hook.chmod(0o755)
    assert _ingest(lane) == 1
    out = capsys.readouterr().out
    recorded = [line for line in out.splitlines() if "recorded" in line]
    assert len(recorded) == 4
    assert all("commit refused" in line for line in recorded)
    assert not any(line.endswith("committed") for line in recorded)
    assert _tracked_call_logs(lane) == []
    assert len(sorted((lane / ITER).glob("call_*.log"))) == 4
