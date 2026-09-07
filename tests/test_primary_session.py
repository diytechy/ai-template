"""Primary session completion gates against real Git turns and trailers."""

import dataclasses
import subprocess
import sys

import pytest

from conftest import SCRIPTS, make_minimal_project, record_ids, run_py, set_process_key

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import agent_loop
import primary_adjudication as primary
import primary_approval
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


def test_session_binding_resolves_real_judgment_and_completes_return(tmp_path):
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
    binding = primary.session_binding(
        root,
        _worker(turn),
        {"phase": "ADJUDICATE", "verdict_path": judgment},
    )
    assert binding["candidate"] == judged
    assert len(binding["candidate"]) == 40
    log = root / "docs/iteration/primary.log"
    log.parent.mkdir(parents=True)
    log.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# base: {}\n"
        "# provider: test\n# roster-row: test\n# model: test\n"
        "# session-id: s\n# invocation-id: i\n".format(turn["base"][:12])
        + "".join("# {}: {}\n".format(k, v) for k, v in binding.items()),
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "primary telemetry")
    records = primary_approval._judgment_records(root, "HEAD", turn, "")
    assert len(records) == 1
    assert records[0][0]["candidate"] == judged
    assert records[0][1] == judgment.read_text(encoding="utf-8")
    end = agent_loop.worker_endstate(root, _worker(turn), False, False, 0, rounds=())
    assert end is not None and end[0] == agent_loop.EXIT_DONE


# Full-tier primary-path proofs. Test-fixture logs model protocol inputs; they
# never claim to be real provider sessions or production approval evidence.
def _review_candidate(tmp_path, mode, draft_class):
    root = tmp_path / "primary"
    root.mkdir()
    boot = run_py([SCRIPTS / "bootstrap.py", "--dest", root], cwd=tmp_path)
    assert boot.returncode == 0, boot.stdout + boot.stderr
    make_minimal_project(root)
    set_process_key(root, "policies", "review_rounds", 1)
    set_process_key(root, "attestation", "adjudication_review", mode)
    spec = root / "docs/work/queued/WI-1-review.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(
        '+++\nid = "WI-1"\ntitle = "Judge the return"\n'
        'workstream = "process"\nsafety_class = "adjudication"\n+++\n'
        "\n## Context\n\nJudge the empty scope.\n",
        encoding="utf-8",
    )
    record_ids(root)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "primary fixture")
    turn = primary.begin(root, "WI-1")
    judgment = root / "docs/reviews/primary-return.md"
    judgment.parent.mkdir(parents=True, exist_ok=True)
    judgment.write_text("OUTCOME: RETURN\n", encoding="utf-8")
    draft = (
        'planmode = "dual"'
        if draft_class == "dual"
        else 'safety_class = "{}"'.format(draft_class)
    )
    spec.write_text(
        spec.read_text(encoding="utf-8")
        + '\n## Approval\n\n```toml\nversion = 1\nturn = "{}"\n'
        'base = "{}"\nproposal = "{}"\ndecision = []\n```\n'.format(
            turn["turn"], turn["base"], verdict.tree_identity(root, turn["base"])
        )
        + '\n## Dispositions\n\n```toml\ntitle = "Continue the returned work"\n'
        'workstream = "process"\nsr_refs = ["SR-001"]\n'
        'supersedes = "WI-1"\nspecref = "docs/reviews/primary-return.md"\n'
        + draft
        + "\n```\n\nPreserve the returned obligation.\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "primary return\n\nWI: WI-1")
    binding = primary.session_binding(
        root, _worker(turn), {"phase": "ADJUDICATE", "verdict_path": judgment}
    )
    log = root / "docs/iteration/primary-test.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# base: {}\n"
        "# provider: test\n# roster-row: fixture\n# model: fixture\n"
        "# session-id: fixture\n# invocation-id: fixture\n".format(turn["base"][:12])
        + "".join("# {}: {}\n".format(k, v) for k, v in binding.items()),
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "fixture primary-session binding")
    return root, turn


def _primary_loop_context(root, turn):
    fields = {field.name: None for field in dataclasses.fields(agent_loop.LoopContext)}
    return dataclasses.replace(
        agent_loop.LoopContext(**fields),
        root=root,
        docs=root / "docs",
        rp_int=1,
        worker=_worker(turn),
        run=agent_loop.LoopRun(routing=agent_loop.RoutingState(1, 900, set(), 3, {})),
    )


def _independent_fixture_round(root):
    reviewed = _git(root, "rev-parse", "HEAD")
    path = root / "docs/reviews/fixture/001-REVIEW-A-{}.md".format(reviewed[:7])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("VERDICT: APPROVE findings=0\n", encoding="utf-8")
    log = root / "docs/iteration/fixture-001-20260101-000000.log"
    log.write_text(
        "# session: 001\n# train: fixture\n# phase: REVIEW-A\n"
        "# outcome: COMMITTED\n# provider: independent-test-fixture\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "fixture independent review")


@pytest.mark.parametrize(
    "mode,draft_class,owed",
    [
        ("never", "ordinary", False),
        ("never", "spine", False),
        ("never", "dual", False),
        ("when-minting", "ordinary", False),
        ("when-minting", "spine", True),
        ("when-minting", "dual", True),
        ("always", "ordinary", True),
        ("always", "spine", True),
        ("always", "dual", True),
    ],
)
def test_pending_primary_review_dial_schedules_and_gates_real_publication(
    tmp_path, mode, draft_class, owed
):
    import primary_publication as publication

    root, turn = _review_candidate(tmp_path, mode, draft_class)
    assert publication.pending(root) == turn
    ctx = _primary_loop_context(root, turn)
    candidate = _git(root, "rev-parse", "HEAD")
    before_files = _git(root, "ls-files")
    agent_loop.build_bookkeeping(
        ctx,
        {
            "phase": "ADJUDICATE",
            "route_id": "fixture",
            "route_family": "test",
            "brief": "",
        },
        "COMMITTED",
        0,
        [candidate],
        candidate,
        turn["wi"],
        0.0,
    )
    st = ctx.run.routing
    assert st.review_queue == (["REVIEW-A"] if owed else [])
    assert st.last_impl_family == ("test" if owed else None)
    assert st.impl_range == ("{}..{}".format(turn["base"], candidate) if owed else None)
    plan, refusal = primary_approval.approval_projection(root, turn)
    assert bool(refusal) is owed
    if owed:
        assert "required independent review phases" in refusal
        closed, refusal = publication.publish(root, turn)
        assert closed is None and "required independent review phases" in refusal
        assert _git(root, "rev-parse", "HEAD") == candidate
        assert _git(root, "ls-files") == before_files
        assert _git(root, "status", "--porcelain") == ""
        _independent_fixture_round(root)
        plan, refusal = primary_approval.approval_projection(root, turn)
    else:
        assert not list((root / "docs/reviews").rglob("*REVIEW-A*"))
    assert refusal is None
    assert (
        plan["outcome"] == "return"
        and plan["statuses"] == {}
        and plan["approves"] == {}
    )
    drafts_before = agent_loop.dispositions_drafted(root, turn["wi"])
    identity = verdict.governing_identity(
        root, "HEAD", carrier=publication.carrier_candidate
    )
    if owed:
        assert agent_loop.review_owed_by_evidence(root, _worker(turn)) == []
    closed, refusal = publication.publish(root, turn)
    assert refusal is None and closed == [turn["wi"]]
    assert publication.pending(root) is None and publication.completed(root, turn)
    assert not (root / turn["spec"]).exists()
    assert (root / "docs/archive/work/complete/WI-1-review.md").is_file()
    assert len(list((root / "docs/work/queued").glob("WI-002-*.md"))) == 1
    assert agent_loop.dispositions_drafted(root, turn["wi"]) == drafts_before
    assert (
        verdict.governing_identity(root, "HEAD", carrier=publication.carrier_candidate)
        == identity
    )
    if owed:
        assert agent_loop.review_owed_by_evidence(root, _worker(turn)) == []
    assert primary.registry_blobs(root, "HEAD") == turn["registry_blobs"]
    assert (
        primary.registry_blobs(root, "HEAD", "docs/archive/last_approved/")
        == turn["approved_blobs"]
    )
    landed = _git(root, "rev-parse", "HEAD")
    assert publication.completed(root, turn)
    assert _git(root, "rev-parse", "HEAD") == landed


@pytest.mark.parametrize("boundary", ["before", "after"])
def test_abrupt_publication_process_exit_preserves_one_completion(tmp_path, boundary):
    import sys
    import primary_publication as publication

    root, turn = _review_candidate(tmp_path, "never", "ordinary")
    candidate = _git(root, "rev-parse", "HEAD")
    # os._exit terminates the publishing process without cleanup/finally at
    # the real git-commit call boundary. This is process loss, not power loss.
    child = r"""
import os, subprocess, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import primary_publication as publication
root = Path(sys.argv[2]); boundary = sys.argv[3]
turn = publication.pending(root)
original = subprocess.run

def run(argv, *args, **kwargs):
    target = (argv[:4] == ["git", "-C", str(root.resolve()), "commit"]
              and any(str(v).startswith("adjudicate: WI-1 primary publication") for v in argv))
    if target and boundary == "before":
        os._exit(88)
    result = original(argv, *args, **kwargs)
    if target and result.returncode == 0 and boundary == "after":
        os._exit(89)
    return result

subprocess.run = run
publication.publish(root, turn)
raise SystemExit("publication never reached the selected boundary")
"""
    proc = subprocess.run(
        [sys.executable, "-c", child, str(SCRIPTS), str(root), boundary],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert proc.returncode == (88 if boundary == "before" else 89), (
        proc.stdout + proc.stderr
    )
    if boundary == "before":
        assert _git(root, "rev-parse", "HEAD") == candidate
        assert publication.pending(root) == turn
        assert _git(root, "status", "--porcelain")
        assert (
            publication.publish(root, turn)[1]
            == "primary is not clean at the exact candidate"
        )
        # Existing supervised recovery: reconcile the interrupted projection
        # to the exact known candidate. No claim of automatic residue cleanup.
        _git(root, "reset", "--hard", candidate)
        assert publication.publish(root, turn) == (["WI-1"], None)
    assert publication.pending(root) is None
    landed = _git(root, "rev-parse", "HEAD")
    assert publication.completed(root, turn)
    assert publication.carrier_candidate(root, landed) == candidate
    assert len(list((root / "docs/work/queued").glob("WI-002-*.md"))) == 1
    assert publication.completed(root, turn)
    assert _git(root, "rev-parse", "HEAD") == landed


def test_primary_engine_holds_writer_exclusion_through_publication(
    tmp_path, monkeypatch
):
    import argparse
    from pathlib import Path
    import agent_common as ac
    import integrate
    import primary_publication as publication

    root, turn = _review_candidate(tmp_path, "always", "spine")
    seen = []

    def excluded(phase):
        seen.append(phase)
        assert (root / "out/integrate.lock").exists()
        assert integrate._claim_refusal(root, ["WI-2"], "competing")
        assert integrate._slot(root)
        assert integrate._slot(root, primary_turn=True)
        with pytest.raises(ValueError, match="pending"):
            primary.begin(root, "WI-1")

    validate = primary.validate

    def at_admission(*args, **kwargs):
        excluded("admission")
        return validate(*args, **kwargs)

    monkeypatch.setattr(primary, "validate", at_admission)

    git = publication._git

    def at_install(repo, *args, **kwargs):
        if Path(repo).resolve() == root.resolve() and args[:2] == (
            "read-tree",
            "--reset",
        ):
            excluded("pre-commit")
        return git(repo, *args, **kwargs)

    monkeypatch.setattr(publication, "_git", at_install)

    def session(args, *, primary_turn):
        assert primary_turn == turn
        excluded("judgment")
        assert (
            "required independent review phases" in publication.publish(root, turn)[1]
        )
        excluded("review")
        _independent_fixture_round(root)
        return ac.EXIT_DONE

    release, why = integrate._dispatch_lock(root)
    assert why is None
    try:
        assert (
            primary.run(root, argparse.Namespace(), session, turn=turn) == ac.EXIT_DONE
        )
    finally:
        release()
    assert {"admission", "judgment", "review", "pre-commit"} <= set(seen)
    assert integrate._slot(root) is None
    ac.release_lock(root / "out/integrate.lock")
    assert publication.pending(root) is None
