import subprocess
import sys
from pathlib import Path

from conftest import SCRIPTS, make_minimal_project, record_ids, run_py, set_process_key

import gen_trajectory
import primary_publication as pp
import primary_adjudication
import handback
from kitlib import stage as kitstage
from kitlib import verdict


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def repo(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.invalid")
    (root / "docs/work/queued").mkdir(parents=True)
    (root / "docs/work/queued/WI-1-x.md").write_text("x\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    return root


def test_completion_rejects_restamped_foreign_tree(tmp_path, monkeypatch):
    root = repo(tmp_path)
    base = git(root, "rev-parse", "HEAD")
    turn = {"turn": "WI-1-" + base, "spec": "docs/work/queued/WI-1-x.md"}
    (root / "docs/work/complete").mkdir(parents=True)
    (root / "docs/work/complete/WI-1-x.md").write_text("closed\n")
    (root / "foreign").write_text("smuggled\n")
    git(root, "add", "-A")
    tree = git(root, "write-tree")
    msg = "x\n\n{}{}\nPublication-Candidate: {}\nPublication-Tree: {}".format(
        pp.TRAILER, turn["turn"], base, tree
    )
    git(root, "commit", "-qm", msg)
    monkeypatch.setattr(pp, "derive_tree", lambda *a, **k: ("0" * 40, [], {}, None))
    assert pp.publication_commit(root, turn) is None


def test_completion_requires_candidate_as_first_parent(tmp_path, monkeypatch):
    root = repo(tmp_path)
    base = git(root, "rev-parse", "HEAD")
    (root / "docs/work/complete").mkdir(parents=True)
    (root / "docs/work/complete/WI-1-x.md").write_text("closed\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "other")
    tree = git(root, "show", "-s", "--format=%T", "HEAD")
    turn = {"turn": "WI-1-" + base, "spec": "docs/work/queued/WI-1-x.md"}
    msg = "x\n\n{}{}\nPublication-Candidate: {}\nPublication-Tree: {}".format(
        pp.TRAILER, turn["turn"], base, tree
    )
    git(root, "commit", "--allow-empty", "-qm", msg)
    monkeypatch.setattr(pp, "derive_tree", lambda *a, **k: (tree, [], {}, None))
    assert pp.publication_commit(root, turn) is None


def test_real_primary_close_moves_exact_queued_spec(tmp_path):
    root = repo(tmp_path)
    spec = root / "docs/work/queued/WI-1-x.md"
    spec.write_text(
        '+++\nid = "WI-1"\ntitle = "clean close"\nsafety_class = "adjudication"\nspecref = "x"\n+++\n\n## Context\n\njudge\n'
    )
    git(root, "add", "-A")
    git(root, "commit", "-qm", "judgment")
    closed, drafts, refusal = handback.stage_primary_adjudication(
        root, "docs/work/queued/WI-1-x.md"
    )
    assert refusal is None and closed == ["WI-1"] and drafts == []
    assert not spec.exists()
    terminal = root / "docs/archive/work/complete/WI-1-x.md"
    text = terminal.read_text()
    assert 'specref = ""' in text
    assert text.index("## Deliverable") < text.index("## Context")


def test_derive_tree_imports_disposable_clone_objects(tmp_path, monkeypatch):
    root = repo(tmp_path)
    candidate = git(root, "rev-parse", "HEAD")

    def project(scratch, turn, cand, tier="all", primary_root=None):
        (Path(scratch) / "derived").write_text("exact\n")
        git(scratch, "add", "-A")
        return ["WI-1"], {"outcome": "return"}, None

    monkeypatch.setattr(pp, "_project", project)
    tree, closed, plan, refusal = pp.derive_tree(root, {}, candidate)
    assert refusal is None and closed == ["WI-1"]
    assert git(root, "cat-file", "-p", tree)


def test_project_runs_candidate_bar_with_primary_harness_python(tmp_path, monkeypatch):
    """Product effects run candidate check.py through the primary checkout venv."""
    primary = tmp_path / "primary"
    scratch = tmp_path / "scratch"
    primary.mkdir()
    scratch.mkdir()
    for root in (primary, scratch):
        git(root, "init", "-q")
        git(root, "config", "user.name", "Test")
        git(root, "config", "user.email", "test@example.invalid")
    sentinel = primary / "harness-used"
    py = primary / ".venv/bin/python"
    py.parent.mkdir(parents=True)
    py.write_text(
        '#!/bin/sh\nprintf used > {!r}\nexec {!r} "$@"\n'.format(
            str(sentinel), sys.executable
        ),
        encoding="utf-8",
    )
    py.chmod(0o755)
    scripts = scratch / "scripts"
    scripts.mkdir()
    (scripts / "trunk_step.py").write_text("pass\n", encoding="utf-8")
    (scripts / "check.py").write_text(
        "import pathlib\n"
        "assert pathlib.Path('candidate-only.txt').is_file()\n"
        "print('  PASS  candidate-check   0.0s')\n",
        encoding="utf-8",
    )
    (scratch / "candidate-only.txt").write_text("product effect\n", encoding="utf-8")
    git(scratch, "add", "-A")
    git(scratch, "commit", "-qm", "candidate")
    candidate = git(scratch, "rev-parse", "HEAD")

    monkeypatch.setattr(pp.primary_turn, "validate_candidate", lambda *_a: None)
    monkeypatch.setattr(
        pp.primary_approval,
        "approval_projection",
        lambda *_a, **_k: (
            {
                "outcome": "return",
                "statuses": {},
                "approves": {},
                "author": None,
                "findings": [],
                "judgment": "docs/reviews/judgment.md",
            },
            None,
        ),
    )
    monkeypatch.setattr(pp, "_apply_approval", lambda *_a: None)

    def stage_product(root, *_a, **_k):
        (Path(root) / "candidate-only.txt").write_text(
            "published product effect\n", encoding="utf-8"
        )
        git(root, "add", "candidate-only.txt")
        return ["WI-1"], [], None

    monkeypatch.setattr(pp.primary_close, "stage_primary_adjudication", stage_product)
    monkeypatch.setattr(pp.intake, "stage_mint", lambda *_a, **_k: ([], None))

    closed, plan, refusal = pp._project(
        scratch,
        {"wi": "WI-1", "spec": "docs/work/queued/WI-1.md"},
        candidate,
        "smoke",
        primary,
    )

    assert refusal is None and closed == ["WI-1"]
    assert plan["verification"]["mode"] == "product-bar"
    assert sentinel.read_text(encoding="utf-8") == "used"


def test_real_return_publish_and_completion_replay(tmp_path, monkeypatch):
    root = repo(tmp_path)
    spec = root / "docs/work/queued/WI-1-x.md"
    spec.write_text(
        '+++\nid = "WI-1"\ntitle = "clean close"\nsafety_class = "adjudication"\nspecref = "x"\n+++\n\n## Context\n\njudge\n'
    )
    step = root / "project-trajectory/scripts/trunk_step.py"
    step.parent.mkdir(parents=True)
    step.write_text("import sys\nsys.exit(0)\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    turn = primary_adjudication.begin(root, "WI-1")
    base = turn["base"]
    turn_id = turn["turn"]
    proposal = verdict.tree_identity(root, base)
    approval = (
        '\n## Approval\n\n```toml\nversion = 1\nturn = "{}"\n'
        'base = "{}"\nproposal = "{}"\ndecision = []\n```\n'
    ).format(turn_id, base, proposal)
    spec.write_text(spec.read_text() + approval)
    log = root / "docs/iteration/WI-1.log"
    log.parent.mkdir(parents=True)
    log.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# base: {}\n# provider: test\n# roster-row: test\n# model: test\n# session-id: s\n# invocation-id: i\n".format(
            base[:12]
        )
    )
    review = root / "docs/reviews/WI-1-001-REVIEW-A.md"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text("VERDICT: APPROVE\nOUTCOME: REVIEWED\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "ADJUDICATE verdict")
    candidate = git(root, "rev-parse", "HEAD")
    log.write_text(
        log.read_text()
        + "# primary-turn: {}\n# judgment: docs/reviews/WI-1-001-REVIEW-A.md\n# candidate: {}\n".format(
            turn_id, candidate
        )
    )
    git(root, "add", "-A")
    git(root, "commit", "-qm", "ADJUDICATE telemetry")
    candidate = git(root, "rev-parse", "HEAD")
    hook = root / ".git/hooks/pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    failed, refusal = pp.publish(root, turn, candidate)
    assert failed is None and "commit failed" in refusal
    assert git(root, "rev-parse", "HEAD") == candidate
    assert git(root, "status", "--porcelain") == ""
    hook.unlink()
    hook.write_text(
        "#!/bin/sh\nprintf 'smuggled\\n' > hook-smuggled\ngit add hook-smuggled\n",
        encoding="utf-8",
    )
    hook.chmod(0o755)
    closed, refusal = pp.publish(root, turn, candidate)
    assert closed is None
    assert refusal == "publication commit tree differs from the verified tree"
    assert git(root, "rev-parse", "HEAD") == candidate
    assert git(root, "status", "--porcelain") == ""
    assert not (root / "hook-smuggled").exists()
    assert not pp.completed(root, turn)
    hook.unlink()
    closed, refusal = pp.publish(root, turn, candidate)
    assert refusal is None and closed == ["WI-1"]
    assert (root / "docs/archive/work/complete/WI-1-x.md").is_file()
    landed = git(root, "rev-parse", "HEAD")
    assert pp.completed(root, turn) and pp.publication_commit(root, turn) == landed
    assert pp.completed(root, turn)  # exact replay is idempotent; no new commit
    assert git(root, "rev-parse", "HEAD") == landed
    # Both readers use the same verified carrier; the reset reader must not.
    identity = verdict.governing_identity(
        root, turn["primary_branch"], candidate, carrier=pp.carrier_candidate
    )
    # Cold identity proof must not fetch objects or rewrite FETCH_HEAD.
    pp._VERIFIED_PUBLICATIONS.clear()
    observed = [root / ".git/FETCH_HEAD", *sorted((root / ".git/objects").rglob("*"))]
    before_objects = {str(p): p.read_bytes() for p in observed if p.is_file()}
    assert pp.carrier_candidate(root, landed) == candidate
    after_paths = [
        root / ".git/FETCH_HEAD",
        *sorted((root / ".git/objects").rglob("*")),
    ]
    assert {
        str(p): p.read_bytes() for p in after_paths if p.is_file()
    } == before_objects
    assert (
        verdict.governing_identity(
            root, turn["primary_branch"], carrier=pp.carrier_candidate
        )
        == identity
    )
    assert verdict.work_tip(root, turn["primary_branch"]) == landed
    message = git(root, "show", "-s", "--format=%B", landed)
    final_tree = git(root, "rev-parse", landed + "^{tree}")
    candidate_tree = git(root, "rev-parse", candidate + "^{tree}")
    for forged_message, forged_tree, parent in (
        (message, candidate_tree, candidate),  # missing the derived effects
        (message, final_tree, landed),  # copied true words onto later work
        (message.replace(turn_id, "WI-999-" + base), final_tree, candidate),
        (message.replace(candidate, base), final_tree, candidate),
        (
            message.replace('"result": "pass"', '"result": "fail"'),
            final_tree,
            candidate,
        ),
        (message + "\n" + pp.TRAILER + turn_id, final_tree, candidate),
    ):
        forged = git(
            root, "commit-tree", forged_tree, "-p", parent, "-m", forged_message
        )
        assert pp.carrier_candidate(root, forged) is None
        if forged_message == message + "\n" + pp.TRAILER + turn_id:
            assert pp._verified_candidate(root, turn, forged) is None
    import os

    bad_author = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "commit-tree",
            final_tree,
            "-p",
            candidate,
            "-m",
            message,
        ],
        env=dict(
            os.environ,
            GIT_AUTHOR_NAME="Wrong author",
            GIT_AUTHOR_EMAIL="wrong@example.invalid",
        ),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert pp.carrier_candidate(root, bad_author) is None
    original_derive = pp.derive_tree
    calls = []

    def counted_derive(*args, **kwargs):
        calls.append(args[2])
        return original_derive(*args, **kwargs)

    monkeypatch.setattr(pp, "derive_tree", counted_derive)
    assert pp.completed(root, turn)
    assert pp.pending(root) is None
    assert calls == []
    mismatched_turn = dict(turn, primary_root="wrong-primary-root")
    assert not pp.completed(root, mismatched_turn)
    assert calls == [candidate]
    calls.clear()
    forged_tree = git(root, "show", "-s", "--format=%T", "HEAD")
    git(
        root,
        "commit",
        "--allow-empty",
        "-qm",
        "forged publication\n\n{}{}\nPublication-Candidate: {}\n"
        "Publication-Tree: {}".format(pp.TRAILER, turn["turn"], landed, forged_tree),
    )
    assert pp.completed(root, turn)
    assert calls == [landed]


def test_bootstrapped_return_publication_replay_keeps_real_regeneration_fresh(
    tmp_path,
):
    root = tmp_path / "scaffold"
    root.mkdir()
    boot = run_py([SCRIPTS / "bootstrap.py", "--dest", root], cwd=tmp_path)
    assert boot.returncode == 0, boot.stdout + boot.stderr
    make_minimal_project(root)
    set_process_key(root, "policies", "review_rounds", 0)
    spec = root / "docs/work/queued/WI-1-return.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(
        '+++\nid = "WI-1"\ntitle = "record a finite return"\n'
        'safety_class = "adjudication"\nspecref = "docs/log.md"\n+++\n'
        "\n## Context\n\nJudge the empty scope.\n",
        encoding="utf-8",
    )
    record_ids(root)
    git(root, "init", "-q")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "seed bootstrapped primary")
    turn = primary_adjudication.begin(root, "WI-1")
    base = turn["base"]
    verdict_path = root / "docs/reviews/WI-1-primary.md"
    verdict_path.parent.mkdir(parents=True, exist_ok=True)
    verdict_path.write_text("OUTCOME: RETURN\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "typed primary return")
    spec.write_text(
        spec.read_text(encoding="utf-8")
        + '\n## Approval\n\n```toml\nversion = 1\nturn = "{}"\n'
        'base = "{}"\nproposal = "{}"\ndecision = []\n```\n'.format(
            turn["turn"], base, verdict.tree_identity(root, base)
        ),
        encoding="utf-8",
    )
    git(root, "add", "-A")
    git(root, "commit", "-qm", "record primary return payload")
    reviewed = git(root, "rev-parse", "HEAD")
    telemetry = root / "docs/iteration/WI-1-primary.log"
    telemetry.parent.mkdir(parents=True, exist_ok=True)
    telemetry.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# provider: test\n"
        "# roster-row: route\n# model: model\n# session-id: session\n"
        "# invocation-id: invocation\n# base: {}\n# primary-turn: {}\n"
        "# judgment: docs/reviews/WI-1-primary.md\n# candidate: {}\n# ---\n".format(
            base[:12], turn["turn"], reviewed
        ),
        encoding="utf-8",
    )
    git(root, "add", "-A")
    git(root, "commit", "-qm", "bind primary return telemetry")
    candidate = git(root, "rev-parse", "HEAD")
    linked = tmp_path / "linked-worker"
    git(root, "worktree", "add", "--detach", str(linked), candidate)
    primary_head = git(root, "rev-parse", "HEAD")
    linked_head = git(linked, "rev-parse", "HEAD")

    closed, refusal = pp.publish(linked, turn, candidate)

    assert closed is None
    assert refusal == "adjudication needs the designated primary checkout"
    assert git(root, "rev-parse", "HEAD") == primary_head
    assert git(linked, "rev-parse", "HEAD") == linked_head
    assert git(root, "status", "--porcelain") == ""
    assert git(linked, "status", "--porcelain") == ""

    closed, refusal = pp.publish(root, turn, candidate)

    assert refusal is None and closed == ["WI-1"]
    landed = git(root, "rev-parse", "HEAD")
    assert pp.completed(root, turn)
    assert git(root, "rev-parse", "HEAD") == landed
    for script in ("derive_stage.py", "gen_trajectory.py"):
        check = subprocess.run(
            [sys.executable, "scripts/" + script, "--check"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        assert check.returncode == 0, check.stdout + check.stderr
    assert git(root, "status", "--porcelain") == ""
    before = {
        path: path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    regen = subprocess.run(
        [sys.executable, "scripts/trunk_step.py", "--root", ".", "--regen"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert regen.returncode == 0, regen.stdout + regen.stderr
    after = {path: path.read_bytes() for path in before}
    dashboard = root / "PROJECT_STATE.html"
    stage = root / "docs/stage"
    # Both writers declare their revision/date comments informational: their
    # --check paths compare dashboard content without ASOF_RE and stage through
    # field_block, because a commit necessarily changes its own as-of identity.
    assert {path for path in before if before[path] != after[path]} == {
        dashboard,
        stage,
    }
    assert gen_trajectory.ASOF_RE.sub("", after[dashboard].decode()) == (
        gen_trajectory.ASOF_RE.sub("", before[dashboard].decode())
    )
    assert kitstage.field_block(kitstage.parse(after[stage].decode())) == (
        kitstage.field_block(kitstage.parse(before[stage].decode()))
    )
    assert pp.completed(root, turn)
    git(root, "checkout", "--", "PROJECT_STATE.html", "docs/stage")
    assert git(root, "status", "--porcelain") == ""


def test_real_first_approval_snapshot_and_successor_are_one_commit(
    tmp_path, monkeypatch
):
    root = repo(tmp_path)
    registry = root / "docs/requirements/low-level-requirements.toml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        '[design.LLR-001]\ntitle="row"\ndetail="detail"\nrationale="why"\nstatus="Drafted"\n'
    )
    snapshot = (
        root
        / "docs/archive/last_approved/docs/requirements/low-level-requirements.toml"
    )
    snapshot.parent.mkdir(parents=True)
    snapshot.write_bytes(registry.read_bytes())
    (root / "docs/process.toml").write_text(
        '[attestation]\nhuman_approval_through="DevStg-Below"\n'
    )
    (root / "docs/id-watermark").write_text("WI = 1\n")
    step = root / "project-trajectory/scripts/trunk_step.py"
    step.parent.mkdir(parents=True)
    step.write_text("import sys\nsys.exit(0)\n")
    spec = root / "docs/work/queued/WI-1-x.md"
    spec.write_text(
        '+++\nid="WI-1"\ntitle="approve"\nsafety_class="adjudication"\nbrief="first-approval"\nspecref="docs/requirements/low-level-requirements.toml"\nadjudicates=["LLR-001"]\n+++\n\n## Context\n\njudge\n'
    )
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    turn = primary_adjudication.begin(root, "WI-1")
    base = turn["base"]
    turn_id = turn["turn"]
    blob = git(
        root, "rev-parse", base + ":docs/requirements/low-level-requirements.toml"
    )
    proposal = verdict.tree_identity(root, base)
    evidence_file = root / "docs/reviews/judgment.md"
    evidence_file.parent.mkdir(parents=True, exist_ok=True)
    evidence_file.write_text("OUTCOME: APPROVE rows=1\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "judgment")
    evidence = git(root, "rev-parse", "HEAD")
    log = root / "docs/iteration/WI-1.log"
    log.parent.mkdir(parents=True)
    log.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# base: {}\n# provider: test\n# roster-row: route\n# model: model\n# session-id: s\n# invocation-id: i\n".format(
            base[:12]
        )
    )
    payload = """\n## Approval\n\n```toml\nversion=1\nturn="{}"\nbase="{}"\nproposal="{}"\n[[decision]]\nregistry="docs/requirements/low-level-requirements.toml"\nrow="LLR-001"\nclassification="approve"\nbefore={{Detail="{}"}}\nafter={{Detail="{}"}}\nevidence=["{}"]\n```\n\n## Dispositions\n\n```toml\ntitle="continue exact work"\nworkstream="process"\nneeds=["WI-1"]\n```\n""".format(
        turn_id, base, proposal, blob, blob, evidence
    )
    spec.write_text(spec.read_text() + payload)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "ADJUDICATE result")
    judged_candidate = git(root, "rev-parse", "HEAD")
    log.write_text(
        log.read_text()
        + "# primary-turn: {}\n# judgment: docs/reviews/judgment.md\n# candidate: {}\n".format(
            turn_id, judged_candidate
        )
    )
    git(root, "add", "-A")
    git(root, "commit", "-qm", "ADJUDICATE telemetry")
    candidate = git(root, "rev-parse", "HEAD")
    monkeypatch.setattr(pp.baseline_snapshot, "_today", lambda: "2001-01-01")
    closed, refusal = pp.publish(root, turn, candidate)
    assert refusal is None and closed == ["WI-1"]
    assert 'status = "Approved"' in registry.read_text()
    assert snapshot.read_bytes() == registry.read_bytes()
    successors = list((root / "docs/work/queued").glob("WI-002-*.md"))
    assert len(successors) == 1 and 'needs = ["WI-1"]' in successors[0].read_text()
    assert "WI = 2" in (root / "docs/id-watermark").read_text()
    monkeypatch.setattr(pp.baseline_snapshot, "_today", lambda: "2099-12-31")
    assert pp.completed(root, turn)  # replay is independent of today's date
    assert git(root, "rev-list", "--count", candidate + "..HEAD") == "1"
