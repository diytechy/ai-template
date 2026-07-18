"""The substance scorer + anti-gaming tripwires + the decayed scoreboard
(score_reviews.py, WI-059). Every scored component is in [0,1]; severity hygiene
and the tripwires are GATES, never scores; length never scores positively."""

from conftest import SCRIPTS, load_script, run_py

score = load_script("score_reviews")


def _write_repo(tmp_path):
    """A tiny repo with two real files so anchors can resolve."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text(
        "\n".join("line" for _ in range(50)), encoding="utf-8"
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "x.md").write_text("# doc\ncontent\n", encoding="utf-8")
    return tmp_path


VERDICT_A = """# Review verdict — REVIEW-A
Model: ANTHROPIC-OPUS-4.8
Role: REVIEW-A

- [MAJOR] src/a.py:12 -> the loop never persists the cooldown -> persist it -> @owner
- [MINOR] docs/x.md:1 -> heading unclear -> reword the heading -> @owner

VERDICT: CHANGES-REQUESTED findings=2
"""

VERDICT_B = """# Review verdict — REVIEW-B
Model: OPENAI-GPT-5.2
Role: REVIEW-B

- [MAJOR] src/a.py:14 -> cooldown state is lost between runs -> keep it in the loop -> @owner
- [MINOR] src/a.py:900 -> nonexistent line anchor -> fix -> @owner

VERDICT: CHANGES-REQUESTED findings=2
"""


def test_parse_verdict_reads_machine_line_and_findings():
    v = score.parse_verdict(VERDICT_A)
    assert v.verdict == "CHANGES-REQUESTED" and v.declared_n == 2
    assert v.model == "ANTHROPIC-OPUS-4.8"
    assert len(v.findings) == 2
    f = v.findings[0]
    assert f.severity == "MAJOR" and f.path == "src/a.py" and f.line == 12
    assert f.change == "persist it"  # the change clause


def test_anchored_precision_penalizes_unresolved_anchor(tmp_path):
    _write_repo(tmp_path)
    v = score.parse_verdict(VERDICT_B)
    # One anchor resolves (a.py:14), one does not (a.py:900 > file length).
    p = score.anchored_precision(v, tmp_path)
    assert p == 0.5


def test_anchored_precision_all_resolve(tmp_path):
    _write_repo(tmp_path)
    v = score.parse_verdict(VERDICT_A)
    assert score.anchored_precision(v, tmp_path) == 1.0


def test_actionability_rate():
    v = score.parse_verdict(VERDICT_A)
    assert score.actionability(v) == 1.0  # both findings carry a change clause
    # A finding with no change clause drops the rate.
    v2 = score.parse_verdict(
        "- [MAJOR] src/a.py:1 -> something is wrong\nVERDICT: CHANGES-REQUESTED findings=1"
    )
    assert score.actionability(v2) == 0.0


def test_corroboration_weights_cross_family_above_same(tmp_path):
    _write_repo(tmp_path)
    va, vb = score.parse_verdict(VERDICT_A), score.parse_verdict(VERDICT_B)
    # a.py:12 (A) vs a.py:14 (B) overlap within the line window -> corroborated.
    cross = score.corroboration(va, vb, providers=("ANTHROPIC", "OPENAI"))
    same = score.corroboration(va, vb, providers=("ANTHROPIC", "ANTHROPIC"))
    assert cross > same > 0
    # A lone reviewer earns no corroboration signal.
    assert score.corroboration(va, None) == 0.0


def test_confirmed_rate_optional_and_scored_when_supplied():
    v = score.parse_verdict(VERDICT_A)
    assert score.confirmed_rate(v, None) is None  # no follow-up diff -> excluded
    # A later commit touched a.py:15 (within +/-10 of the a.py:12 finding).
    r = score.confirmed_rate(v, {"src/a.py": {15}})
    assert 0 < r <= 1


def test_substance_is_mean_of_available_components_length_never_positive(tmp_path):
    _write_repo(tmp_path)
    va, vb = score.parse_verdict(VERDICT_A), score.parse_verdict(VERDICT_B)
    s = score.substance(va, tmp_path, other=vb, providers=("ANTHROPIC", "OPENAI"))
    assert 0.0 <= s <= 1.0
    # A padded, low-substance review (many words, no resolvable/actionable finding)
    # must not out-score a lean substantive one.
    padded = score.parse_verdict(
        "Model: X\n" + "a " * 500 + "\nVERDICT: APPROVE findings=0"
    )
    lean = score.parse_verdict(VERDICT_A)
    assert score.substance(padded, tmp_path) <= 1.0
    assert (
        score.substance(lean, tmp_path, other=vb, providers=("ANTHROPIC", "OPENAI")) > 0
    )


def test_tripwire_count_mismatch():
    good = score.parse_verdict(VERDICT_A)  # declared 2, counted 2
    assert not score.tripwire_count_mismatch(good)
    bad = score.parse_verdict(
        "- [MAJOR] src/a.py:1 -> x -> y\nVERDICT: CHANGES-REQUESTED findings=9"
    )
    assert score.tripwire_count_mismatch(bad)


def test_tripwire_near_duplicate():
    assert score.tripwire_near_duplicate(
        "fix the cooldown bug now", "fix the cooldown bug now"
    )
    assert not score.tripwire_near_duplicate(
        "the cooldown is never persisted", "the module map is stale in the readme"
    )


def test_tripwire_implementer_touched_review_path():
    assert score.tripwire_implementer_touched_review(["docs/reviews/012-REVIEW-A.md"])
    assert score.tripwire_implementer_touched_review(["docs/review-policy"])
    assert not score.tripwire_implementer_touched_review(["src/a.py", "docs/x.md"])


def test_tripwire_covers_meta_repo_kit_script_layout():
    # WI-167: the routing referees live at project-trajectory/scripts/ in this
    # meta-repo, so a downstream-only prefix would miss an implementer editing
    # the scorer/router here. Both layouts must fire.
    assert score.tripwire_implementer_touched_review(
        ["project-trajectory/scripts/score_reviews.py"]
    )
    assert score.tripwire_implementer_touched_review(
        ["project-trajectory/scripts/agent_route.py"]
    )
    # Windows-style separators normalise to the same match.
    assert score.tripwire_implementer_touched_review(
        ["project-trajectory\\scripts\\agent_route.py"]
    )
    # A sibling kit script that is not a routing referee still does not fire.
    assert not score.tripwire_implementer_touched_review(
        ["project-trajectory/scripts/trace.py"]
    )


def test_tripwire_mass_rejection():
    assert score.tripwire_mass_rejection(rejected=3, total=4)
    assert not score.tripwire_mass_rejection(rejected=1, total=4)
    assert not score.tripwire_mass_rejection(rejected=0, total=0)


def test_merge_verdict_mechanical_no_debate():
    va, vb = score.parse_verdict(VERDICT_A), score.parse_verdict(VERDICT_B)
    merged, contra = score.merge_verdict([va, vb])
    assert merged == "CHANGES-REQUESTED" and contra is False
    approve = score.parse_verdict("VERDICT: APPROVE findings=0")
    merged2, contra2 = score.merge_verdict([approve, va])
    assert merged2 == "CHANGES-REQUESTED" and contra2 is True  # they disagreed


def test_fired_tripwires_aggregates():
    va = score.parse_verdict(VERDICT_A)
    bad = score.parse_verdict(
        "- [MAJOR] src/a.py:1 -> x -> y\nVERDICT: APPROVE findings=5"
    )
    fired = score.fired_tripwires([va, bad], changed_paths=["docs/review-policy"])
    assert "finding-count-mismatch" in fired
    assert "implementer-touched-review-path" in fired


def test_scoreboard_roundtrip_and_decay(tmp_path):
    sb = tmp_path / "reviews" / "scoreboard.txt"
    score.record_round(
        sb,
        {
            "verdict": "CHANGES-REQUESTED",
            "tier": "strong",
            "margin": 0,
            "primary": None,
            "tripwire": False,
            "contradiction": False,
        },
        {"ANTHROPIC": 0.8},
    )
    score.record_round(
        sb,
        {
            "verdict": "APPROVE",
            "tier": "strong",
            "margin": 2,
            "primary": "OPENAI",
            "tripwire": False,
            "contradiction": False,
        },
        {"ANTHROPIC": 0.5, "OPENAI": 0.9},
    )
    providers, rounds = score.read_scoreboard(sb)
    # Decayed: 0.8*0.7 + 0.5 = 1.06 for ANTHROPIC over two rounds.
    assert abs(providers["ANTHROPIC"][0] - 1.06) < 1e-6
    assert providers["ANTHROPIC"][1] == 2
    assert len(rounds) == 2
    assert rounds[1]["verdict"] == "APPROVE" and rounds[1]["primary"] == "OPENAI"
    assert rounds[1]["margin"] == 2


def test_cli_scores_and_records(tmp_path):
    # The Provides-CLI seam (IF-046): score a verdict file and record the round.
    (tmp_path / "work.txt").write_text("only one line\n", encoding="utf-8")
    v = tmp_path / "v.md"
    v.write_text(
        "- [MINOR] work.txt:1 -> a nit -> tidy it -> @owner\nVERDICT: APPROVE findings=1\n",
        encoding="utf-8",
    )
    sb = tmp_path / "scoreboard.txt"
    proc = run_py(
        [
            SCRIPTS / "score_reviews.py",
            "--verdict",
            v,
            "--root",
            tmp_path,
            "--provider",
            "PROVA",
            "--tier",
            "medium",
            "--scoreboard",
            sb,
            "--record",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "substance=" in proc.stdout and "recorded round" in proc.stdout
    assert sb.exists() and "provider PROVA" in sb.read_text(encoding="utf-8")


def test_cli_exit_1_on_tripwire(tmp_path):
    # A declared findings count that does not match the lines fires a tripwire ->
    # the CLI exits 1 (a non-scored gate).
    v = tmp_path / "v.md"
    v.write_text(
        "- [MAJOR] x -> y -> z\nVERDICT: CHANGES-REQUESTED findings=7\n",
        encoding="utf-8",
    )
    proc = run_py(
        [SCRIPTS / "score_reviews.py", "--verdict", v, "--root", tmp_path], cwd=tmp_path
    )
    assert proc.returncode == 1
    assert "finding-count-mismatch" in proc.stdout
