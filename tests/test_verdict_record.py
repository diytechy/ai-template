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
    """Raw, split `git ls-tree -r -z` entries — `fold_listing`'s input."""
    return [
        "100644 blob {:040x}\t{}".format(i, p).encode() for i, p in enumerate(paths, 1)
    ]


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
    changed_code = [entry.replace(b"00001", b"00009") for entry in base]
    assert kv.fold_listing(base) != kv.fold_listing(changed_code)
    assert kv.fold_listing(base) != kv.fold_listing(_listing("src/widget.py"))


def test_a_record_path_is_excluded_whatever_characters_it_holds(tmp_path):
    # ROUND 007, FINDING 3, driven through git rather than asserted about it.
    # Without `-z`, git QUOTES a path holding a non-ASCII character
    # (`"docs/log.d/WI-401-café.md"`), the leading quote defeats every
    # RECORD_PREFIXES test, and one accented log fragment silently stales every
    # governing verdict on the branch — the exact class the exclusion exists to
    # prevent. The identity must not move when such a file lands.
    root = git_repo(tmp_path)
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: the widget", when=T_CODE)
    before = kv.tree_identity(root, "HEAD")

    frag = root / "docs" / "log.d" / "WI-401-café.md"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text("## 2026-01-01 — café\n", encoding="utf-8", newline="\n")
    _commit(root, "log: an accented fragment", when=T_LATER)
    assert "\\303" in _git(root, "ls-tree", "-r", "HEAD"), (
        "the fixture must actually reproduce git's quoting, or it proves nothing"
    )
    assert kv.tree_identity(root, "HEAD") == before

    # ...and the other answer: an accented WORK path still moves it.
    (root / "src" / "café.py").write_text("VALUE = 2\n", encoding="utf-8", newline="\n")
    _commit(root, "feat: an accented module", when=T_LATER + 100)
    assert kv.tree_identity(root, "HEAD") != before


def test_distinct_invalid_utf8_work_paths_have_distinct_identities(monkeypatch):
    # ROUND 019: replacement-decoding the complete NUL stream made one blob at
    # byte-distinct work paths look identical, so a R100 rename could leave a
    # stale APPROVE governing. Drive the exact collision without asking a
    # Windows filesystem to represent POSIX's arbitrary filename bytes.
    meta = b"100644 blob 078e25798f331e5d407065dc9c0725f8ad166332d\t"
    listings = {"before": meta + b"src/\x80\0", "after": meta + b"src/\x81\0"}
    assert listings["before"].decode(errors="replace") == listings["after"].decode(
        errors="replace"
    ), "the fixture must reproduce the replacement-decoding collision"
    monkeypatch.setattr(kv, "git_bytes", lambda _root, args: listings[args[-1]])

    assert kv.tree_identity("unused", "before") != kv.tree_identity("unused", "after")


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


def test_round_count_counts_cycles_not_reviewers():
    entries = [
        ("REVIEW-A", 3, "CHANGES-REQUESTED"),
        ("REVIEW-B", 4, "CHANGES-REQUESTED"),
        ("REVIEW-A", 5, "APPROVE"),
        ("REVIEW-B", 6, "APPROVE"),
    ]
    assert kv.round_count(entries[:2]) == 1
    assert kv.round_count(entries) == 2


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


def test_a_trailer_contradicting_the_governing_round_count_refuses(tmp_path):
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
        + kv.format_trailer("APPROVE", 0, tree),
    )
    _git(root, "checkout", "-q", "main")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "APPROVE rounds=0" in refusal
    assert "APPROVE rounds=1" in refusal


def _stamp(root, tree, word, rounds, when):
    """One coordinator attestation, on the telemetry commit shape that carries
    it: record-only, so the commit's own non-record identity IS `tree`."""
    (root / "docs" / "reviews" / "wi-401" / "scoreboard.txt").write_text(
        "rounds {}\n".format(rounds), encoding="utf-8", newline="\n"
    )
    _commit(
        root,
        "telemetry: session {:03d} review scoreboard\n\n".format(rounds)
        + kv.format_trailer(word, rounds, tree),
        when=when,
    )


def test_the_newest_attestation_at_a_tree_governs_the_cross_check(tmp_path):
    # ROUND 007, FINDING 1. `git log` is NEWEST-first, so a last-write-wins map
    # handed the gate the OLDEST stamp: two honest rounds at one governing tree
    # (`rounds=1`, then `rounds=2`) made the cross-check report the attestation
    # and the evidence as disagreeing and park an approved lane at a supervisor
    # stop — the OI-76 failure mode, re-created by the check meant to prevent
    # it, and reachable on any re-drawn round.
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    tree = kv.governing_identity(root, "wi-401")
    _stamp(root, tree, "APPROVE", 1, T_LATER + 100)
    _git(root, "checkout", "-q", "main")
    add_round(root, 5, when=T_LATER + 200)  # a second round, same tree
    _git(root, "checkout", "-q", "wi-401")
    assert kv.governing_identity(root, "wi-401") == tree, (
        "record-only commits must not have moved the tree under judgement"
    )
    _stamp(root, tree, "APPROVE", 2, T_LATER + 300)
    _git(root, "checkout", "-q", "main")

    assert kv.branch_trailers(root, "wi-401", _rev(root, "main"))[tree] == [
        ("APPROVE", 1),
        ("APPROVE", 2),
    ], "the attestations arrive as a sequence, oldest first — not one per tree"
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def _refresh_commit(root, branch, when):
    """A GENUINE station refresh commit on `branch`: trunk content folded in,
    with the `Bar-Green:` trailer naming its own tree and its work parent, which
    is what `refresh_attestation` verifies. Written by hand rather than through
    `integrate.refresh` because the lane worktree/bar machinery is not what is
    under test here — the peel is."""
    work = _rev(root, branch)
    (root / "trunk.txt").write_text("from trunk\n", encoding="utf-8", newline="\n")
    _commit(root, "placeholder", when=when)
    tree = _rev(root, "HEAD^{tree}")
    _git(
        root,
        "commit",
        "-q",
        "--amend",
        "--no-edit",
        "-m",
        "{}0123456789\n\nBar-Green: tree={} work={} bar green".format(
            kv.refresh_subject(branch), tree, work
        ),
    )
    assert kv.refresh_attestation(root, branch) == (work, "bar green")
    return work


def test_a_station_refresh_owes_no_round_and_the_two_readers_agree(tmp_path):
    # ROUND 007, FINDING 2. The gate measured the identity at the PEELED work
    # tip and the loop's derivation at HEAD, so "one definition, two readers"
    # (WI-560 DW1) held for every commit class except the one the peel exists
    # for. On a refreshed branch the loop answered "owed" while the gate was
    # already satisfied, and the resumed lane drew a strong-tier round whose
    # file the gate would not even read.
    al = _al()
    root = rounds_repo(tmp_path)
    _git(root, "checkout", "-q", "wi-401")
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "WI-401: close\n\nWI: WI-401", when=T_CODE + 50)
    _git(root, "checkout", "-q", "main")
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    base = _rev(root, "main")
    worker = {"train": "wi-401", "assigned": ["WI-401"], "base": base, "rework": ""}
    assert al.review_owed_by_evidence(root, worker) is False

    work = _refresh_commit(root, "wi-401", T_LATER + 100)
    # The refresh REALLY moved the tree — without this the test would pass on a
    # peel that did nothing.
    assert kv.tree_identity(root, "HEAD") != kv.tree_identity(root, work)
    assert kv.governing_identity(root, "wi-401") == kv.tree_identity(root, work)

    assert al.review_owed_by_evidence(root, worker) is False, (
        "a mechanical refresh must not re-owe a round the lane already served"
    )
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def _record_commit(root, ordinal, when):
    """One coordinator telemetry commit — a RECORD path and nothing else."""
    _git(root, "checkout", "-q", "wi-401")
    log = (
        root
        / "docs"
        / "iteration"
        / "wi-401-{:03d}-20260101-000001.log".format(ordinal)
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("# phase: BUILD\n", encoding="utf-8", newline="\n")
    _commit(root, "telemetry: session wi-401-{:03d} BUILD".format(ordinal), when=when)


def test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel(tmp_path):
    # The peel used to be TIP-ONLY, because it is shared with the `reset --hard`
    # in `integrate.refresh`, where peeling one commit too far destroys work. So
    # a telemetry commit landing on top of a refresh made the tip stop being a
    # refresh commit, the peel stopped applying, and the identity flipped to the
    # post-refresh tree. The fold already ignores `docs/iteration/`, so the
    # commit could not move the identity by itself — it moved it by HIDING the
    # refresh. An APPROVE served before the refresh then named nothing, and both
    # readers agreed on the wrong answer: the OI-76 failure mode, one commit
    # further down than the round-007 fix reached.
    al = _al()
    root = rounds_repo(tmp_path)
    _git(root, "checkout", "-q", "wi-401")
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "WI-401: close\n\nWI: WI-401", when=T_CODE + 50)
    _git(root, "checkout", "-q", "main")
    add_round(root, 3)
    base = _rev(root, "main")
    worker = {"train": "wi-401", "assigned": ["WI-401"], "base": base, "rework": ""}
    _git(root, "checkout", "-q", "wi-401")
    served = kv.governing_identity(root, "wi-401")

    work = _refresh_commit(root, "wi-401", T_LATER + 100)
    _record_commit(root, 4, T_LATER + 200)
    assert kv.tree_identity(root, "HEAD") != kv.tree_identity(root, work), (
        "the refresh must really have moved the tree, or this proves nothing"
    )
    gov = kv.governing_rev(root, "wi-401")
    assert gov != _rev(root, "wi-401"), "the walk must not stop at the tip"
    assert kv.tree_identity(root, gov) == kv.tree_identity(root, work), (
        "the governing rev names the PRE-refresh work tree, not the tree the "
        "telemetry commit left on the tip"
    )
    assert kv.governing_identity(root, "wi-401") == served
    assert al.review_owed_by_evidence(root, worker) is False, (
        "the coordinator's own telemetry must not re-owe a served round"
    )
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None

    # ...and the OTHER carrier, which is the one the coordinator actually
    # writes for an attestation (ROUND 012, FINDING 1). `commit_telemetry`
    # commits EMPTY when a `Review-Verdict:` trailer must land on unchanged
    # bookkeeping — a zero-path commit, which is precisely what a walk that
    # CLASSIFIES PATHS cannot classify and so used to stop at, burying the
    # refresh under it exactly as the non-empty case above once did. Driven
    # through the producer rather than a hand-made lookalike, so the two stay
    # tied: if `commit_telemetry` ever stops writing this shape the test says
    # so instead of quietly testing a shape nothing emits.
    _git(root, "checkout", "-q", "wi-401")
    ac.commit_telemetry(
        root,
        "wi-401-005",
        "REVIEW-A COMMITTED",
        [],
        trailer=kv.format_trailer("APPROVE", 1, served),
    )
    assert not _git(root, "show", "--format=", "--name-only", "HEAD").strip(), (
        "the fixture must really reproduce the EMPTY carrier, or it proves "
        "nothing about the shape that produced the finding"
    )
    assert kv.governing_identity(root, "wi-401") == served, (
        "an empty commit changes no tree, so it cannot move the identity — and "
        "it must not move it by hiding the refresh either"
    )
    assert al.review_owed_by_evidence(root, worker) is False
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None

    # The opposite, without which the walk could peel everything and pass: a
    # WORK commit above the refresh is not walked through, and it does re-owe.
    _git(root, "checkout", "-q", "wi-401")
    (root / "src" / "widget.py").write_text(
        "VALUE = 3\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "WI-401: more work\n\nWI: WI-401", when=T_LATER + 300)
    _record_commit(root, 5, T_LATER + 400)
    assert kv.governing_identity(root, "wi-401") != served
    assert al.review_owed_by_evidence(root, worker) is True
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is not None


def test_the_empty_carrier_commits_its_own_paths_and_never_the_index(tmp_path):
    # ROUND 015, FINDING 2. The empty-carrier arm SWAPPED the commit's pathspec
    # for `--allow-empty`, and a `git commit` with no pathspec reads THE INDEX.
    # So one unrelated staged file — a state this function's own `pre_staged`
    # restore already treats as reachable — landed inside a commit labelled
    # `telemetry:`, carrying a `Review-Verdict:` attestation on a commit that
    # changed the work tree. Silent wrong content under a bookkeeping label,
    # and an attestation whose "an empty commit changes no tree" premise was
    # simply false. The pre-diff form was immune by construction, so the fix is
    # to keep the path scope on BOTH arms rather than to guard the index.
    root = rounds_repo(tmp_path)
    _git(root, "checkout", "-q", "wi-401")
    scoreboard = root / "docs" / "reviews" / "wi-401" / "scoreboard.txt"
    scoreboard.parent.mkdir(parents=True, exist_ok=True)
    scoreboard.write_text("rounds 1\n", encoding="utf-8", newline="\n")
    _commit(root, "telemetry: the scoreboard, already current", when=T_LATER)

    # UNRELATED work, staged and uncommitted, with the bookkeeping unchanged —
    # the exact state that produced the finding.
    (root / "src" / "unrelated.py").write_text(
        "VALUE = 9\n", encoding="utf-8", newline="\n"
    )
    _git(root, "add", "--", "src/unrelated.py")
    ac.commit_telemetry(
        root,
        "wi-401-002",
        "REVIEW-A COMMITTED",
        [scoreboard],
        trailer=kv.format_trailer("APPROVE", 1, "0" * 64),
    )
    assert _git(root, "log", "-1", "--format=%s").strip() == (
        "telemetry: session wi-401-002 REVIEW-A COMMITTED"
    )
    assert not _git(root, "show", "--format=", "--name-only", "HEAD").strip(), (
        "the attestation's carrier must be EMPTY — an unrelated staged file "
        "swept into it is work landing under a bookkeeping label"
    )
    assert _git(root, "diff", "--cached", "--name-only").split() == [
        "src/unrelated.py"
    ], "the caller's index must be left exactly as it was found"

    # ...AND WITH NO PATHS AT ALL, which is the arm the round-015 fix did not
    # reach: it kept the pathspec on both arms of the `dirty` test, but the
    # pathspec is appended only `if rels`, so `paths=[]` still emitted a
    # pathspec-less `git commit --allow-empty` — the very shape the finding was
    # about. Not a hypothetical call: this suite makes it twice, and it is what
    # a caller with nothing to record but an attestation writes.
    ac.commit_telemetry(
        root,
        "wi-401-003",
        "REVIEW-A COMMITTED",
        [],
        trailer=kv.format_trailer("APPROVE", 1, "0" * 64),
    )
    assert not _git(root, "show", "--format=", "--name-only", "HEAD").strip(), (
        "a carrier with no paths must commit NOTHING — reading the index here "
        "is the same work-under-a-bookkeeping-label defect, one branch over"
    )
    assert _git(root, "diff", "--cached", "--name-only").split() == [
        "src/unrelated.py"
    ], "and the index is still left exactly as it was found"


def test_a_round_drawn_after_a_refresh_is_visible_to_both_readers(tmp_path):
    # ROUND 015, THE BLOCKER — and the OTHER ORDER of the test above, which is
    # the whole reason it was invisible. That one refreshes AFTER the round;
    # this one draws the round AFTER the refresh, which is what the shipped
    # path actually produces: `dispatch._advance` spawns a lane's refresh as
    # soon as its worker is DONE and BEFORE `integrate.integrate` runs, so any
    # slot refusal parks the branch with a refresh commit and no round, and the
    # next launch's `resume_owed_round` draws the round on top of it.
    #
    # The reviewer then reads — and its round file cites — the POST-refresh sha,
    # while both readers govern by the PEELED pre-refresh tree. Binding the
    # round with a raw `tree_identity` made those two permanently unequal: no
    # commit on the branch could make them match short of new work, the gate
    # refused "no logged review round names its current tree", and the loop
    # re-owed the round it had just served — an identical round every tick,
    # which is the double-identical-round class WI-560 DW1 claims to have made
    # unrepresentable. A round is now bound by the SAME composed definition the
    # gate governs by.
    al = _al()
    root = rounds_repo(tmp_path)
    _git(root, "checkout", "-q", "wi-401")
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "WI-401: close\n\nWI: WI-401", when=T_CODE + 50)
    base = _rev(root, "main")
    worker = {"train": "wi-401", "assigned": ["WI-401"], "base": base, "rework": ""}

    work = _refresh_commit(root, "wi-401", T_LATER + 100)
    assert kv.tree_identity(root, "HEAD") != kv.tree_identity(root, work), (
        "the refresh must really have moved the tree, or this proves nothing"
    )
    refresh_sha = _rev(root, "wi-401")
    _git(root, "checkout", "-q", "main")
    reviewed = add_round(root, 3)
    assert reviewed == refresh_sha[:7] != work[:7], (
        "the fixture must draw the round at the POST-refresh tip — the whole "
        "finding is that the reviewed sha is not the governing one"
    )

    _git(root, "checkout", "-q", "wi-401")
    assert al.review_owed_by_evidence(root, worker) is False, (
        "a round drawn after the refresh SERVED the lane; re-owing it is the "
        "double-identical-round class re-entered through the binding"
    )
    # ...and the trailer the coordinator stamps for that round lands under the
    # key the cross-check looks it up by (round 015, finding 5): writer and both
    # readers name ONE value, so the cross-check cross-checks instead of
    # silently standing down.
    want = kv.governing_identity(root, "wi-401")
    trailer = al.review_verdict_trailer(root, "APPROVE", worker)
    assert kv.parse_trailer(trailer) == ("APPROVE", 1, want)
    ac.commit_telemetry(root, "wi-401-004", "REVIEW-A COMMITTED", [], trailer=trailer)
    assert kv.branch_trailers(root, "wi-401", base).get(want) == [("APPROVE", 1)]

    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None

    # The opposite, without which a binding that peeled everything would pass:
    # rework after the round still re-owes one.
    _git(root, "checkout", "-q", "wi-401")
    (root / "src" / "widget.py").write_text(
        "VALUE = 3\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "WI-401: rework\n\nWI: WI-401", when=T_LATER + 300)
    assert al.review_owed_by_evidence(root, worker) is True
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is not None


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
    #
    # ROUND 007, FINDING 4: and it must not claim N APPROVALS either. Every
    # completed round is appended to the tally whatever its merged verdict, so a
    # lane that took a CHANGES-REQUESTED round, reworked and then passed drew
    # two rounds and was approved once. The banner says what the tally carries.
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

    reworked = [{"verdict": "CHANGES-REQUESTED"}, {"verdict": "APPROVE"}]
    _code, _label, drew = al.worker_endstate(
        str(root), worker, False, True, 1, rounds=reworked
    )
    assert "2 review round(s) drawn this run, latest verdict APPROVE" in drew
    assert "approved" not in drew, "two rounds were drawn; one of them approved"
    _code, _label, none = al.worker_endstate(
        str(root), worker, False, True, 1, rounds=[]
    )
    assert "no review round was drawn this run" in none
    assert "approved" not in none


def test_the_trailer_count_is_derived_at_the_governing_tree(tmp_path):
    al = _al()
    root = rounds_repo(tmp_path)
    add_round(root, 3)
    _git(root, "checkout", "-q", "wi-401")
    worker = {
        "train": "wi-401",
        "assigned": ["WI-401"],
        "base": _rev(root, "main"),
        "rework": "",
    }
    first = kv.parse_trailer(al.review_verdict_trailer(root, "APPROVE", worker))
    assert first is not None and first[1] == 1

    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: rework", when=T_LATER + 100)
    add_round(root, 5, when=T_LATER + 200)
    _git(root, "checkout", "-q", "wi-401")
    second = kv.parse_trailer(al.review_verdict_trailer(root, "APPROVE", worker))
    assert second is not None and second[1] == 1


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
    assert al.review_owed_by_evidence(root, worker) is True
    add_round(root, 4, session_phase="BUILD")
    _git(root, "checkout", "-q", "wi-401")
    assert al.review_owed_by_evidence(root, worker) is True
    _git(root, "checkout", "-q", "main")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is not None
    add_round(root, 5)
    _git(root, "checkout", "-q", "wi-401")
    assert al.review_owed_by_evidence(root, worker) is False

    # THE CLASS ITSELF: record-only commits after the verdict re-owe nothing.
    frag = root / "docs" / "log.d" / "WI-401-widget.md"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text("## 2026-01-01 — widget\n", encoding="utf-8", newline="\n")
    (reviews / "scoreboard.txt").write_text(
        "rounds 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "telemetry: session 006 review scoreboard", when=T_LATER + 200)
    assert al.review_owed_by_evidence(root, worker) is False


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

    # THE THIRD ANSWER, and the arm that was UNCOVERED while it was broken
    # (round 015). A retired review scope leaves an EXTRA rollup behind; the
    # `--check` arm reported it and the write path never removed it, so the
    # remedy the failure message names could not clear the failure — an
    # unbreakable red on the pre-commit floor and in `_TRUNK_FRESHNESS_STEPS`,
    # under a misleading instruction. The generator OWNS the directory now, so
    # what matters is not that STALE is reported but that regenerating clears
    # it.
    assert gen.main(["--root", str(root)]) == 0
    assert gen.main(["--root", str(root), "--check"]) == 0
    retired = root / "docs" / "reviews" / "rollup" / "wi-999.md"
    retired.write_text("# a scope that no longer exists\n", encoding="utf-8")
    assert gen.main(["--root", str(root), "--check"]) == 1, "an extra is stale"
    assert gen.main(["--root", str(root)]) == 0
    assert not retired.exists(), (
        "the regenerator the failure message names must be able to clear it"
    )
    assert gen.main(["--root", str(root), "--check"]) == 0
