"""Primary session completion gates against real Git turns and trailers."""

import subprocess
import sys

from conftest import SCRIPTS

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import agent_loop
import primary_adjudication as primary
from kitlib import verdict


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "user.email", "test@example.invalid")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8")
    spec = root / "docs/work/queued/WI-1-judge.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(
        '+++\nid = "WI-1"\ntitle = "Judge"\nworkstream = "process"\n'
        'safety_class = "adjudication"\n+++\n\n## Context\n\nJudge.\n',
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "base")
    return root


def _worker(turn):
    return {
        "assigned": [turn["wi"]],
        "base": turn["base"],
        "train": turn["primary_branch"],
        "primary_turn": turn,
        "adjudication_owed": "",
        "rework": "",
    }


def test_wi_trailer_without_primary_approval_stays_in_rework(tmp_path):
    root = _repo(tmp_path)
    turn = primary.begin(root, "WI-1")
    _git(root, "commit", "--allow-empty", "-qm", "judgment\n\nWI: WI-1")
    end = agent_loop.worker_endstate(root, _worker(turn), False, False, 0, rounds=())
    assert end is None
    refusal = primary.completion_refusal(root, _worker(turn))
    assert refusal and "Approval" in refusal


def test_valid_primary_return_can_complete_the_judgment_turn(tmp_path):
    root = _repo(tmp_path)
    turn = primary.begin(root, "WI-1")
    proposal = verdict.tree_identity(root, turn["base"])
    spec = root / turn["spec"]
    judgment = root / "docs/reviews/judgment.md"
    judgment.parent.mkdir(parents=True, exist_ok=True)
    judgment.write_text("OUTCOME: RETURN\nWI: WI-1\n", encoding="utf-8")
    spec.write_text(
        spec.read_text(encoding="utf-8")
        + "\n## Approval\n\n```toml\n"
        + 'version = 1\nturn = "{}"\nbase = "{}"\nproposal = "{}"\n'.format(
            turn["turn"], turn["base"], proposal
        )
        + "decision = []\n```\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "judgment\n\nWI: WI-1")
    judged = _git(root, "rev-parse", "HEAD")
    log = root / "docs/iteration/primary.log"
    log.parent.mkdir(parents=True)
    log.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# base: {}\n"
        "# provider: test\n# roster-row: test\n# model: test\n"
        "# session-id: s\n# invocation-id: i\n# primary-turn: {}\n"
        "# judgment: docs/reviews/judgment.md\n# candidate: {}\n".format(
            turn["base"][:12], turn["turn"], judged
        ),
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "primary telemetry")
    end = agent_loop.worker_endstate(root, _worker(turn), False, False, 0, rounds=())
    assert end is not None and end[0] == agent_loop.EXIT_DONE
