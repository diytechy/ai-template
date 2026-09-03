"""The verdict record (OI-76): tree identity, the round evidence, the trailer,
and the `adjudication_review` dial.

WHAT THIS MODULE IS FOR. The ruling of 2026-08-31 replaced a hand-authored
rollup and a commit-TIME comparison with two things a test can actually pin: a
verdict is EVIDENCE a logged reviewer session produced, and it counts only while
it NAMES the tree it judged. Both halves are failure-shaped — a rule that only
ever answers "yes" on the happy path is not a rule — so every case below is
asserted alongside its opposite:

  * the identity ignores record paths AND notices work paths;
  * a round from a logged reviewer session counts AND an implementer-authored
    file in the same directory does not (the plan's finding K);
  * a verdict that names this tree clears the gate AND one that named an
    earlier tree does not;
  * the `Review-Verdict:` trailer is a CROSS-CHECK, so one that contradicts the
    rounds refuses — the trailer alone never clears anything;
  * the dial's three values, and the case the whole row exists for: an
    adjudication lane merging with NO verdict file anywhere.
"""

import sys

import pytest
from conftest import SCRIPTS, load_script
from integrate_fixtures import (
    T_BASE,
    T_CODE,
    T_LATER,
    _commit,
    _git,
    _rev,
    git_repo,
    write_spec,
)

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kv  # noqa: E402

ac = load_script("agent_common")
integ = load_script("integrate")

APPROVE = "# Review A\n\nModel: test/reviewer\n\nVERDICT: APPROVE findings=0\n"
CHANGES = (
    "# Review A\n\nModel: test/reviewer\n\n"
    "- [MAJOR] src/widget.py:1 -> wrong -> fix it -> @owner\n\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)

LOG = "# agent-loop session log\n# session: {ordinal:03d}\n# train: {train}\n# phase: {phase}\n# outcome: COMMITTED\n"


# --- 1. the identity, as a pure fold -----------------------------------------


def _listing(*paths):
    return "".join(
        "100644 blob {:040x}\t{}\n".format(i, p) for i, p in enumerate(paths, 1)
    )


def test_the_identity_ignores_every_record_path():
    # The three record directories are the process writing about ITSELF. If a
    # round file, a log fragment or a session log could change the identity,
    # the very act of recording a verdict would invalidate it — which is
    # precisely the double-identical-round defect measured on WI-547.
    work = _listing("src/widget.py")
    with_records = work + _listing(
        "docs/reviews/wi-401/003-REVIEW-A-abc1234.md",
        "docs/log.d/WI-401-widget.md",
        "docs/iteration/wi-401-003-20260101-000000.log",
    )
    assert kv.fold_listing(work) == kv.fold_listing(with_records)


def test_the_identity_notices_work_and_notices_docs_work():
    # The other answer, without which the test above would pass on a fold that
    # ignored everything. `docs/work/` is IN the identity deliberately (WI-378
    # measured the price): a spec's safety_class, needs and Deliverable are the
    # claims a verdict is ABOUT, and letting them move unseen after an APPROVE
    # is the case the exclusion would have bought.
    base = _listing("src/widget.py", "docs/work/active/wi-401/WI-401-widget.md")
    changed_code = _listing(
        "src/widget.py", "docs/work/active/wi-401/WI-401-widget.md"
    ).replace("00001", "00009")
    assert kv.fold_listing(base) != kv.fold_listing(changed_code)
    assert kv.fold_listing(base) != kv.fold_listing(_listing("src/widget.py"))


# --- 2. the trailer grammar ---------------------------------------------------


def test_the_trailer_round_trips_and_the_last_one_governs():
    tree = "a" * 64
    line = kv.format_trailer("APPROVE", 2, tree)
    assert line == "Review-Verdict: APPROVE rounds=2 tree=" + tree
    # A rework commit that QUOTES the round it answers must not have the
    # quotation read as its own attestation; the kit's convention puts a
    # commit's own trailers last.
    quoted = (
        "rework\n\nanswering Review-Verdict: APPROVE rounds=1 tree={}\n\n{}".format(
            "b" * 64, kv.format_trailer("CHANGES-REQUESTED", 3, tree)
        )
    )
    assert kv.parse_trailer(quoted) == ("CHANGES-REQUESTED", 3, tree)


@pytest.mark.parametrize(
    "line",
    [
        "Review-Verdict: MAYBE rounds=1 tree=" + "a" * 64,  # not in the enum
        "Review-Verdict: APPROVE rounds=1 tree=" + "a" * 40,  # a git tree sha
        "Review-Verdict: APPROVE tree=" + "a" * 64,  # no round count
    ],
)
def test_a_malformed_trailer_is_no_trailer(line):
    # Fail to PARSE rather than parse to something. An unrecognized verdict word
    # arriving downstream as a third outcome is a state nobody wrote a rule for.
    assert kv.parse_trailer("subject\n\n" + line) is None


def test_round_and_session_names_parse_including_the_relaxed_tag():
    assert kv.round_file("docs/reviews/wi-401/003-REVIEW-A-abc1234.md") == (
        "wi-401",
        3,
        "REVIEW-A",
        "abc1234",
    )
    # C5 records a relaxed-heterogeneity draw in the NAME; it is still a round.
    assert kv.round_file("docs/reviews/wi-401/007-REVIEW-B-abc1234-relaxed.md") == (
        "wi-401",
        7,
        "REVIEW-B",
        "abc1234",
    )
    # The pre-train flat layout has no train directory.
    assert kv.round_file("docs/reviews/003-REVIEW-A-abc1234.md") == (
        "",
        3,
        "REVIEW-A",
        "abc1234",
    )
    # The hand-authored rollup is NOT a round file — it names no reviewed sha,
    # which is exactly why it could never be bound to a tree.
    assert kv.round_file("docs/reviews/WI-401-REVIEW-A.md") is None
    assert kv.session_log("docs/iteration/wi-401-003-20260101-000000.log") == (
        "wi-401",
        3,
    )


# --- 3. the gate over round evidence ------------------------------------------


def rounds_repo(tmp_path):
    """A trunk with the review dial on, and `wi-401` carrying one code commit.

    The TRUNK is left checked out, as it is when the station runs: the gate
    resolves the branch's own commits against `merge-base(HEAD, branch)`, and a
    fixture sitting on the branch would hand it an empty range."""
    root = git_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "review-policy").write_text("1\n", encoding="utf-8", newline="\n")
    _commit(root, "declare the review policy", when=T_BASE)
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: the widget", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    return root


def add_round(root, ordinal, text=APPROVE, session_phase="REVIEW-A", when=T_LATER):
    """Commit one round on `wi-401`: the coordinator's session log AND the
    reviewer's verdict file, named for the code HEAD it read."""
    _git(root, "checkout", "-q", "wi-401")
    sha = (_rev(root, "wi-401") or "")[:7]
    log = (
        root
        / "docs"
        / "iteration"
        / "wi-401-{:03d}-20260101-000000.log".format(ordinal)
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(
        LOG.format(ordinal=ordinal, train="wi-401", phase=session_phase),
        encoding="utf-8",
        newline="\n",
    )
    rnd = (
        root
        / "docs"
        / "reviews"
        / "wi-401"
        / "{:03d}-REVIEW-A-{}.md".format(ordinal, sha)
    )
    rnd.parent.mkdir(parents=True, exist_ok=True)
    rnd.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "review: round {}".format(ordinal), when=when)
    _git(root, "checkout", "-q", "main")
    return sha


def test_a_logged_reviewer_round_naming_this_tree_clears_the_gate(tmp_path):
    # The whole point of the row: no hand-authored rollup exists anywhere, and
    # the branch merges anyway. Before this, `docs/reviews/WI-401-REVIEW-A.md`
    # was required and nothing in the kit wrote it, so every mechanized lane
    # stopped at a human.
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    assert not (root / "docs" / "reviews" / "WI-401-REVIEW-A.md").exists()
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_an_implementer_authored_file_in_the_review_path_is_not_a_round(tmp_path):
    # THE PLAN'S FINDING K, closed. A BUILD session on WI-538 really did write
    # `010-REVIEW-A-e26ab03.md` — an implementer authoring its own approval.
    # Harmless while the gate ignored round files; a counted round under a naive
    # compile. The join is to the COORDINATOR's committed session log, which the
    # session cannot write for itself.
    root = rounds_repo(tmp_path)
    add_round(root, 3, session_phase="BUILD")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "no logged review round" in refusal


def test_a_round_that_judged_an_earlier_tree_does_not_count(tmp_path):
    # Identity, not ordering: the round is the LATEST thing on the branch by
    # commit time and still does not count, because the tree it named is gone.
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: rework after the round", when=T_LATER + 100)
    _git(root, "checkout", "-q", "main")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "no logged review round" in refusal


def test_a_record_only_commit_after_the_round_leaves_it_governing(tmp_path):
    # The other answer to the test above, and the defect it retires: the loop's
    # own telemetry, the scoreboard and a log fragment all land AFTER a round
    # and none of them changed the work. Under the retired time comparison each
    # one re-owed a round; under identity they cannot.
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    frag = root / "docs" / "log.d" / "WI-401-widget.md"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text("## 2026-01-01 — widget\n", encoding="utf-8", newline="\n")
    (root / "docs" / "reviews" / "wi-401" / "scoreboard.txt").write_text(
        "rounds 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "telemetry: session 004 review scoreboard", when=T_LATER + 100)
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_the_governing_round_can_refuse(tmp_path):
    root = rounds_repo(tmp_path)
    add_round(root, 3, text=CHANGES)
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "not an APPROVE" in refusal


def test_a_trailer_contradicting_the_rounds_refuses(tmp_path):
    # The trailer is the machine half and a CROSS-CHECK, never an accept path.
    # A merge slot that saw an attestation disagreeing with the evidence and
    # merged anyway would be trusting the summary over the evidence all over
    # again — the exact inversion OI-76 was filed about.
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    tree = kv.tree_identity(root, "wi-401")
    _git(
        root,
        "commit",
        "-q",
        "--allow-empty",
        "-m",
        "telemetry: session 004 review scoreboard\n\n"
        + kv.format_trailer("CHANGES-REQUESTED", 1, tree),
    )
    _git(root, "checkout", "-q", "main")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "attestation and the evidence disagree" in refusal


# --- 4. the adjudication_review dial ------------------------------------------


def _docs(tmp_path, mode):
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "process.toml").write_text(
        '[attestation]\nadjudication_review = "{}"\n'.format(mode),
        encoding="utf-8",
        newline="\n",
    )
    return docs


@pytest.mark.parametrize(
    "mode,brief,drafts,owed",
    [
        # never: not even a consolidation earns a second opinion.
        ("never", "consolidate", ["spine"], False),
        # when-minting: the verdict creates exclusive work, or moves scope.
        ("when-minting", "amendment", ["spine"], True),
        ("when-minting", "red-tc", ["high-risk"], True),
        ("when-minting", "consolidate", [], True),
        # ...and the cases the policy exists to SKIP: a flip recommendation, a
        # red-tc drafting ordinary fix rows, a clean-close spot check.
        ("when-minting", "amendment", [], False),
        ("when-minting", "red-tc", ["ordinary", "ordinary"], False),
        ("when-minting", "", [], False),
        # always: the intended-but-broken behaviour, made real.
        ("always", "", [], True),
    ],
)
def test_the_dial_decides_when_an_adjudication_owes_a_round(
    tmp_path, mode, brief, drafts, owed
):
    assert ac.adjudication_review_owed(_docs(tmp_path, mode), brief, drafts) is owed


def test_an_unreadable_dial_falls_to_when_minting_not_to_never(tmp_path):
    # The failure that matters is silently reviewing NOTHING. A typo is a `str`,
    # so the type check cannot see it; `config_conflicts` refuses it loudly
    # upstream and this reader falls back conservatively for anyone who did not
    # run that gate.
    assert ac.adjudication_review(_docs(tmp_path, "nevr")) == "when-minting"
    assert ac.adjudication_review_owed(_docs(tmp_path, "nevr"), "", ["spine"]) is True


def adjudication_repo(tmp_path, mode, drafts_class="ordinary"):
    """A closed ADJUDICATION lane whose verdict drafts one successor."""
    root = rounds_repo(tmp_path)
    (root / "docs" / "process.toml").write_text(
        '[attestation]\nadjudication_review = "{}"\n'.format(mode),
        encoding="utf-8",
        newline="\n",
    )
    spec = write_spec(
        root, "active/wi-401", "WI-401", safety="adjudication", brief="amendment"
    )
    _commit(root, "claim: WI-401", when=T_CODE)
    _git(root, "checkout", "-q", "wi-401")
    _git(root, "merge", "-q", "main", "-m", "merge trunk")
    landed = root / "docs" / "archive" / "work" / "complete" / spec.name
    landed.parent.mkdir(parents=True, exist_ok=True)
    landed.write_text(
        spec.read_text(encoding="utf-8")
        + "\n## Dispositions\n\n```toml\n"
        'title = "the successor"\nworkstream = "process"\n'
        'safety_class = "{}"\n```\n\nThe successor\'s scope.\n'.format(drafts_class),
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "work" / "active" / "wi-401" / spec.name).unlink()
    _commit(root, "WI-401: rule and close", when=T_LATER)
    _git(root, "checkout", "-q", "main")
    return root


@pytest.mark.parametrize("mode", ["never", "when-minting"])
def test_an_adjudication_lane_owing_no_round_merges_with_no_verdict_file(
    tmp_path, mode
):
    # THE MEASUREMENT THE WHOLE ROW EXISTS FOR (OI-76's acceptance). Before the
    # dial, `_verdict_gate` demanded `docs/reviews/WI-401-REVIEW-A.md` from a
    # lane whose phase is in NON_BUILD_PHASES — so nothing produced one, and
    # every adjudication merge was a supervisor stop. Here the lane holds NO
    # verdict artifact of any kind and the gate is satisfied.
    root = adjudication_repo(tmp_path, mode, drafts_class="ordinary")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_a_minting_adjudication_still_owes_its_round(tmp_path):
    # The other answer: a spine successor runs exclusive and touches the
    # registries, which is where a second opinion earns its cost.
    root = adjudication_repo(tmp_path, "when-minting", drafts_class="spine")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "no logged review round" in refusal


# --- 5. the loop side: the honest banner, the shared derivation, the rollup ---


def _al():
    return load_script("agent_loop")


def test_the_done_banner_states_the_rounds_it_actually_drew(tmp_path):
    # WI-559 DW2's second half. The banner used to read "review round approved"
    # whenever managed routing ran at policy >= 1 — true of a build, false of
    # every adjudication, which drew no round at all. Three lanes on the
    # 2026-08-31 run exited DONE claiming an approval nobody had given.
    al = _al()
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    _git(root, "checkout", "-q", "-b", "t1")
    (root / "work.txt").write_text("work\n", encoding="utf-8", newline="\n")
    _git(root, "add", "-A")
    _git(
        root,
        "commit",
        "-q",
        "-m",
        "build\n\nWI: WI-401\nTrain: t1\nBase: {}\n".format(base),
    )
    worker = {"train": "t1", "assigned": ["WI-401"], "base": base, "rework": ""}

    _code, _label, drew = al.worker_endstate(
        str(root), worker, False, True, 1, rounds=2
    )
    assert "2 review round(s) approved" in drew
    _code, _label, none = al.worker_endstate(
        str(root), worker, False, True, 1, rounds=0
    )
    assert "no review round was drawn" in none
    assert "approved" not in none


def test_the_review_owed_derivation_and_the_gate_share_one_definition(tmp_path):
    # WI-560 DW1, driven on the class it exists to kill. The loop's own
    # telemetry and log fragments moved HEAD past a verdict on WI-547 and this
    # derivation re-owed a round it had already been served, drawing two
    # identical `APPROVE findings=0` rounds. Both readers now compare the SAME
    # non-record tree identity, so the record commits below cannot re-owe it.
    al = _al()
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    base = _rev(root, "main")
    worker = {"train": "wi-401", "assigned": ["WI-401"], "base": base, "rework": ""}
    reviews = root / "docs" / "reviews" / "wi-401"

    # The train's WI trailer is what makes the lane BUILT; without it no round
    # is owed for a reason that has nothing to do with the verdict. This commit
    # also REWORKS the code, so the round drawn above no longer names this tree
    # and one is genuinely owed; a fresh round then serves it.
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "WI-401: rework and close\n\nWI: WI-401", when=T_LATER + 100)
    assert al.review_owed_by_evidence(root, worker, reviews) is True
    add_round(root, 5)
    _git(root, "checkout", "-q", "wi-401")
    assert al.review_owed_by_evidence(root, worker, reviews) is False

    # THE CLASS ITSELF: record-only commits after the verdict re-owe nothing.
    frag = root / "docs" / "log.d" / "WI-401-widget.md"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text("## 2026-01-01 — widget\n", encoding="utf-8", newline="\n")
    (reviews / "scoreboard.txt").write_text(
        "rounds 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "telemetry: session 006 review scoreboard", when=T_LATER + 200)
    assert al.review_owed_by_evidence(root, worker, reviews) is False


def test_the_rollup_is_generated_and_its_check_has_two_answers(tmp_path):
    # DW3: the rollup dies as an INPUT and is reborn generated. `--check` is
    # what keeps it honest — a generated artifact nobody regenerates is a
    # document that lies, and this one is read by humans deciding whether a
    # lane was reviewed.
    gen = load_script("gen_verdict_rollup")
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")

    assert gen.main(["--root", str(root), "--check"]) == 1  # absent is stale
    assert gen.main(["--root", str(root)]) == 0
    rollup = root / "docs" / "reviews" / "rollup" / "wi-401.md"
    assert "REVIEW-A" in rollup.read_text(encoding="utf-8")
    # The gate never reads it, and the file says so where a human will see it.
    assert "The merge gate does\nnot read this file." in rollup.read_text(
        encoding="utf-8"
    )
    assert gen.main(["--root", str(root), "--check"]) == 0

    add_round(root, 5, text=CHANGES)
    _git(root, "checkout", "-q", "wi-401")
    assert gen.main(["--root", str(root), "--check"]) == 1
