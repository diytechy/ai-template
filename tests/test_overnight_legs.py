"""The overnight-leg launcher, in process (`scripts/coordinator/overnight_legs.py`,
this repository's own tooling): the run's marker, the leg prompt's
composition and the refusals before any leg.

No git and no process is spawned here: the handoff reader, the lease reader
and the agent CLI's resolution are replaced. The real-repository cases, with
stub legs, are in `test_overnight_legs_git.py`.
"""

import os
import re
import shutil
import sys

import agent_brief
import agent_common
import pytest
from conftest import KIT
from kitlib import provenance

from overnight_legs_fixtures import BLOCK, LOOP_SESSION_ENV, handoff_text, load_launcher

WELL_FORMED = "20260101T000000Z-abcdef"


@pytest.fixture
def ol(tmp_path, monkeypatch):
    """The launcher, logging under `tmp_path`, with `sys.path` restored. The
    kit's shared readers it calls answer from the same fake: the trunk reader
    names `main`, and `agent_common.git` runs through the launcher's
    `run_git`, in `git()`'s own `(code, out)` shape."""
    monkeypatch.setattr(sys, "path", list(sys.path))
    module = load_launcher()
    monkeypatch.setattr(module, "LOGDIR", tmp_path / "logs")
    monkeypatch.setattr(module, "lease_holder", lambda repo: None)
    monkeypatch.setattr(agent_common, "trunk_name", lambda repo: "main")

    def kit_git(root, *args):
        code, out, err = module.run_git(root, list(args))
        out, err = (out or "").strip(), (err or "").strip()
        if code != 0 and err:
            out = out + "\n" + err if out else err
        return code, out

    monkeypatch.setattr(agent_common, "git", kit_git)
    return module


def unreached(calls):
    """A handoff reader that records being called: the leg loop was reached."""

    def newest_handoff(repo):
        calls.append(repo)
        return None

    return newest_handoff


def log_text(ol):
    path = ol.LOGDIR / "loop.log"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def test_the_prompt_is_the_session_prompt_then_the_block_then_the_provenance_line(ol):
    note = "\n\nLOOP PROVENANCE: end every commit with `Loop-Session: s-1`."
    prompt = ol.leg_prompt(
        "You are the coordinator.", "\n  CHECK the marker.\nGo on.\n\n", note
    )
    assert prompt == "You are the coordinator.\n\nCHECK the marker.\nGo on." + note


def write_bad_block(path, shape):
    if shape == "directory":
        path.mkdir()
    elif shape == "non-utf8":
        path.write_bytes(b"\xff\xfe\x00bad")
    elif shape == "empty":
        path.write_text("", encoding="utf-8")
    elif shape == "whitespace":
        path.write_text(" \n\t\n", encoding="utf-8")


@pytest.mark.parametrize(
    "shape, reason",
    [
        ("absent", "absent"),
        ("directory", "unreadable"),
        ("non-utf8", "not UTF-8"),
        ("empty", "empty"),
        ("whitespace", "empty"),
    ],
)
def test_a_missing_unreadable_or_empty_block_refuses_the_run_before_any_leg(
    ol, tmp_path, monkeypatch, shape, reason
):
    block = tmp_path / "headless-leg.md"
    write_bad_block(block, shape)
    monkeypatch.setattr(ol, "HEADLESS_BLOCK", block, raising=False)
    calls = []
    monkeypatch.setattr(ol, "newest_handoff", unreached(calls))
    assert ol.main(["--repo", str(tmp_path)]) == 2
    stop = [line for line in log_text(ol).splitlines() if "stop:" in line]
    assert stop and str(block) in stop[-1] and reason in stop[-1]
    assert calls == []


def test_an_empty_provenance_note_refuses_the_run_before_any_leg(
    ol, tmp_path, monkeypatch
):
    block = tmp_path / "headless-leg.md"
    block.write_text("Check the marker.\n", encoding="utf-8")
    monkeypatch.setattr(ol, "HEADLESS_BLOCK", block, raising=False)
    monkeypatch.setattr(agent_brief, "loop_provenance_note", lambda: "")
    calls = []
    monkeypatch.setattr(ol, "newest_handoff", unreached(calls))
    assert ol.main(["--repo", str(tmp_path)]) == 2
    assert "provenance note" in log_text(ol)
    assert calls == []


@pytest.mark.parametrize("inherited", [None, WELL_FORMED, "not a session!"])
def test_the_run_marks_itself_once_keeping_a_well_formed_inherited_marker(
    ol, tmp_path, monkeypatch, inherited
):
    if inherited is not None:
        monkeypatch.setenv(LOOP_SESSION_ENV, inherited)
    handoff = tmp_path / "handoff-001.md"
    handoff.write_text(handoff_text(1), encoding="utf-8")
    monkeypatch.setattr(ol, "newest_handoff", lambda repo: handoff)
    monkeypatch.setattr(shutil, "which", lambda name, *a, **k: str(tmp_path / name))
    assert ol.main(["--repo", str(tmp_path), "--dry-run"]) == 0
    session = os.environ.get(LOOP_SESSION_ENV)
    assert (
        session and provenance.mark_loop_process({LOOP_SESSION_ENV: session}) == session
    )
    assert (session == inherited) == (inherited == WELL_FORMED)
    assert "run session {}".format(session) in log_text(ol)


# --- the after-leg audit and check-lane, over a fake git runner ---------------
# Trunk `main` moves A -> B in the leg, `archive/lanes` C -> D, and the leg
# creates the lane `wi-1` at L. Each read site answers from FakeGit's table.
A, B, C, D, L = ("a" * 40, "b" * 40, "c" * 40, "d" * 40, "1" * 40)
X, Y, T = ("2" * 40, "3" * 40, "4" * 40)
TRUNK = "refs/heads/main"
ARCHIVE = "refs/heads/archive/lanes"
PRE = {TRUNK: A, ARCHIVE: C}
OTHER = "20250101T000000Z-0a0b0c"
CLAIM = "claim: WI-1 -> active/wi-1 (bookkeeping)"
RECLAIM = "reclaim: wi-1 (attended)"  # the re-claim subject the kit composes


def marked(subject, session=WELL_FORMED):
    return "{}\n\nLoop-Session: {}".format(subject, session)


def records(*commits):
    """`git log --format=%H%x00%B%x1e` output for `(sha, message)` pairs."""
    return "".join("{}\x00{}\n\x1e\n".format(sha, msg) for sha, msg in commits)


TREE_B = "5" * 40  # the tree of trunk's tip B, the lane's boundary parent
EMPTY = "empty"  # a lane commit whose tree is its parent's


def lane_log(*commits):
    """The lane read's `git log --boundary` output for `(sha, message)` or
    `(sha, message, EMPTY)` commits on one line of descent from trunk's tip B:
    B is the boundary record, each commit's parent is the one before it, and
    each commit's tree is its own unless it is EMPTY."""
    out = ["-\x00{}\x00\x00{}\x00trunk tip\n\x1e\n".format(B, TREE_B)]
    parent, parent_tree = B, TREE_B
    for sha, message, *empty in commits:
        tree = parent_tree if empty else "e" + sha[1:]
        out.append(
            ">\x00{}\x00{}\x00{}\x00{}\n\x1e\n".format(sha, parent, tree, message)
        )
        parent, parent_tree = sha, tree
    return "".join(out)


def snapshot_out(refs):
    return "".join("{} {}\n".format(sha, ref) for ref, sha in refs.items())


def ok(out=""):
    return (0, out, "")


FAILED = (128, "", "fatal: bad object")


class FakeGit:
    """A git runner answering each read site from a table: `answers[site]` is
    a `(code, stdout, stderr)` triple."""

    def __init__(self, **answers):
        self.answers = {
            "name": ok(TRUNK + "\n"),
            "snapshot": ok(snapshot_out({TRUNK: B, ARCHIVE: D, "refs/heads/wi-1": L})),
            "descent": ok(),
            "archive-descent": ok(),
            "trunk": ok(records((B, marked("handoff: leg 1")))),
            "archive": ok(records((D, marked("archive record")))),
            "lane": ok(lane_log((L, marked("lane work")))),
            "claim": ok(records((B, marked(CLAIM)))),
            "resolve": ok(L + "\n"),
            "trunk-tip": ok(B + "\n"),
        }
        self.answers.update(answers)

    @staticmethod
    def site(args):
        if args[0] != "log":
            simple = {"symbolic-ref": "name", "for-each-ref": "snapshot"}
            if args[0] == "rev-parse":
                return "trunk-tip" if TRUNK in " ".join(args) else "resolve"
            if args[0] == "merge-base" and C in args:
                return "archive-descent"
            return simple.get(args[0], "descent")
        if any(a.startswith("--grep") for a in args):
            return "claim"
        if "--topo-order" in args:
            return "lane"
        return "trunk" if "{}..{}".format(A, B) in args else "archive"

    def __call__(self, repo, args):
        return self.answers[self.site(list(args))]


def audit_with(ol, monkeypatch, pre=PRE, **answers):
    """Run the snapshot before a leg and the audit after it over FakeGit."""
    monkeypatch.setattr(ol, "run_git", FakeGit(**answers), raising=False)
    ol.pre_leg("repo", TRUNK)
    summary, _post = ol.audit("repo", TRUNK, pre, WELL_FORMED)
    return summary


@pytest.mark.parametrize(
    "site, named",
    [
        ("name", "symbolic-ref"),
        ("snapshot", "for-each-ref"),
        ("descent", "merge-base"),
        ("trunk", "{}..{}".format(A, B)),
        ("archive", "{}..{}".format(C, D)),
        ("lane", "{}..refs/heads/wi-1".format(B)),
        # A pin: the claim is read through the kit's shared claim reader, and
        # a failed read stops the audit, as the launcher's own copy did.
        ("claim", "--grep"),
    ],
)
def test_every_failed_audit_read_stops_the_run_naming_the_read(
    ol, monkeypatch, site, named
):
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, **{site: FAILED})
    assert type(stop.value).__name__ == "AuditStop"
    assert named in str(stop.value) and "exit 128" in str(stop.value)


def test_a_failed_range_read_is_never_an_empty_range(ol, monkeypatch):
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, lane=(128, "", ""))
    assert type(stop.value).__name__ == "AuditStop"
    assert "wi-1" in audit_with(ol, monkeypatch, lane=ok(""))


@pytest.mark.parametrize(
    "answers",
    [
        {"snapshot": ok("abc123 refs/heads/main\n")},
        {"lane": ok("not-a-sha\x00lane work\n\x1e\n")},
        {
            "lane": ok(
                ">\x00not-a-sha\x00{}\x00{}\x00lane work\n\x1e\n".format(B, TREE_B)
            )
        },
        {"lane": ok("?\x00{}\x00{}\x00{}\x00lane work\n\x1e\n".format(L, B, TREE_B))},
        {"lane": ok(">\x00{}\x00{}\x00lane work\n\x1e\n".format(L, B))},
    ],
    ids=["snapshot", "lane-old-shape", "lane-sha", "lane-mark", "lane-fields"],
)
def test_unparseable_read_output_stops_the_run(ol, monkeypatch, answers):
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, **answers)
    assert type(stop.value).__name__ == "AuditStop"
    assert "unparseable" in str(stop.value)


@pytest.mark.parametrize(
    "answers, named",
    [
        ({"resolve": (128, "", "fatal: no such ref")}, "wi-1"),
        ({"lane": FAILED}, "{}..refs/heads/wi-1".format(B)),
        # A pin: the shared claim reader's failed read refuses the landing.
        ({"claim": FAILED}, "--grep"),
    ],
)
def test_check_lane_refuses_when_a_read_fails(ol, monkeypatch, capsys, answers, named):
    monkeypatch.setattr(ol, "run_git", FakeGit(**answers), raising=False)
    assert ol.check_lane("repo", "wi-1") == 3
    assert named in capsys.readouterr().out


CHECKOUT_CASES = {
    "another branch": (ok("refs/heads/elsewhere\n"), "elsewhere"),
    "detached": ((1, "", ""), "detached"),
    "unparseable": (ok("garbage\n"), "unparseable"),
    "failed read": (FAILED, "symbolic-ref"),
}


@pytest.mark.parametrize("case", sorted(CHECKOUT_CASES))
def test_the_checkout_must_stay_on_the_bound_trunk(ol, monkeypatch, case):
    answer, named = CHECKOUT_CASES[case]
    monkeypatch.setattr(ol, "run_git", FakeGit(name=answer), raising=False)
    with pytest.raises(Exception) as before:
        ol.pre_leg("repo", TRUNK)
    with pytest.raises(Exception) as after:
        ol.audit("repo", TRUNK, PRE, WELL_FORMED)
    for stop in (before.value, after.value):
        assert type(stop).__name__ == "AuditStop"
        assert named in str(stop)


def test_the_audit_names_a_refused_commit_before_the_checkout(ol, monkeypatch):
    fake = FakeGit(
        name=ok("refs/heads/elsewhere\n"),
        trunk=ok(records((B, "unmarked trunk work"))),
    )
    monkeypatch.setattr(ol, "run_git", fake, raising=False)
    with pytest.raises(Exception) as stop:
        ol.audit("repo", TRUNK, PRE, WELL_FORMED)
    assert B[:10] in str(stop.value) and "elsewhere" not in str(stop.value)


def test_a_snapshot_without_the_bound_trunk_stops_before_the_leg(ol, monkeypatch):
    # A pin: a trunk no local branch holds was a stop before the leg already.
    fake = FakeGit(snapshot=ok(snapshot_out({ARCHIVE: D})))
    monkeypatch.setattr(ol, "run_git", fake, raising=False)
    with pytest.raises(Exception) as stop:
        ol.pre_leg("repo", TRUNK)
    assert type(stop.value).__name__ == "AuditStop" and TRUNK in str(stop.value)


def ready_to_run(ol, tmp_path, monkeypatch):
    """Everything `prepare_run` reads before the bind resolves, and the log
    folder `main` makes."""
    ol.LOGDIR.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv(LOOP_SESSION_ENV, WELL_FORMED)
    monkeypatch.setattr(shutil, "which", lambda name, *a, **k: str(tmp_path / name))


def test_the_bind_reads_trunk_once_and_logs_it(ol, tmp_path, monkeypatch):
    ready_to_run(ol, tmp_path, monkeypatch)
    calls = []
    monkeypatch.setattr(
        agent_common, "trunk_name", lambda repo: calls.append(repo) or "main"
    )
    prepared = ol.prepare_run(tmp_path)
    assert prepared[-1] == TRUNK and calls == [tmp_path]
    assert "run trunk main" in log_text(ol)


def test_a_value_error_from_the_trunk_reader_stops_the_run(ol, tmp_path, monkeypatch):
    ready_to_run(ol, tmp_path, monkeypatch)

    def refusing(repo):
        raise ValueError("trunk undeclared: probe")

    monkeypatch.setattr(agent_common, "trunk_name", refusing)
    calls = []
    monkeypatch.setattr(ol, "newest_handoff", unreached(calls))
    assert ol.main(["--repo", str(tmp_path)]) == 2
    assert "trunk undeclared: probe" in log_text(ol) and calls == []


def test_check_lane_cannot_judge_when_the_trunk_reader_refuses(ol, monkeypatch, capsys):
    def refusing(repo):
        raise ValueError("trunk undeclared: probe")

    monkeypatch.setattr(agent_common, "trunk_name", refusing)
    monkeypatch.setattr(ol, "run_git", FakeGit(), raising=False)
    assert ol.check_lane("repo", "wi-1") == 3
    out = capsys.readouterr().out
    assert "cannot judge" in out and "trunk undeclared: probe" in out


def test_check_lane_cannot_judge_when_the_trunk_reader_names_no_branch(
    ol, monkeypatch, capsys
):
    fake = FakeGit()

    def run_git(repo, args):
        if args[0] == "rev-parse" and "refs/heads/nosuch^{commit}" in args:
            return 128, "", "fatal: Needed a single revision"
        return fake(repo, args)

    monkeypatch.setattr(agent_common, "trunk_name", lambda repo: "nosuch")
    monkeypatch.setattr(ol, "run_git", run_git, raising=False)
    assert ol.check_lane("repo", "wi-1") == 3
    out = capsys.readouterr().out
    assert "cannot judge" in out and "refs/heads/nosuch" in out


def test_the_leg_log_line_prints_the_bound_trunks_tips(ol, tmp_path, monkeypatch):
    fake = FakeGit()
    snapshots = [ok(snapshot_out(PRE))]

    def run_git(repo, args):
        if args[0] == "for-each-ref" and snapshots:
            return snapshots.pop(0)
        return fake(repo, args)

    monkeypatch.setattr(ol, "run_git", run_git, raising=False)
    monkeypatch.setattr(ol, "run_leg", lambda *args: 0)
    ol.LOGDIR.mkdir(parents=True)
    out = tmp_path / "leg.log"
    assert ol.run_and_audit("repo", 1, ["claude"], "p", out, WELL_FORMED, TRUNK) is None
    assert "leg 1 exit 0; trunk {} -> {}".format(A[:8], B[:8]) in log_text(ol)


def test_an_unparseable_claim_record_stops_the_audit(ol, monkeypatch):
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, claim=ok("not-a-sha\x00claim\n\x1e\n"))
    assert type(stop.value).__name__ == "AuditStop"
    assert "unparseable" in str(stop.value) and "--grep" in str(stop.value)


@pytest.mark.parametrize(
    "pre, answers, named",
    [
        (PRE, {"trunk": ok(records((B, "unmarked trunk work")))}, B[:10]),
        (PRE, {"trunk": ok(records((B, marked("foreign", OTHER))))}, B[:10]),
        (PRE, {"descent": (1, "", "")}, A[:10]),
        # A pin: an archive the leg creates is judged over the commits no
        # pre-leg branch reaches, as before.
        (
            {TRUNK: A},
            {"archive": ok(records((D, "unmarked archive record")))},
            D[:10],
        ),
    ],
    ids=["unmarked", "foreign", "rewind", "archive-absent-before"],
)
def test_the_trunk_rule_refuses_an_unmarked_or_foreign_commit_and_a_rewind(
    ol, monkeypatch, pre, answers, named
):
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, pre=pre, **answers)
    assert type(stop.value).__name__ == "AuditStop"
    assert named in str(stop.value)


ARCHIVE_GONE = ok(snapshot_out({TRUNK: B, "refs/heads/wi-1": L}))


@pytest.mark.parametrize(
    "answers",
    [{"archive-descent": (1, "", "")}, {"snapshot": ARCHIVE_GONE}],
    ids=["not-descending", "deleted"],
)
def test_the_archive_must_descend_from_its_pre_leg_tip(ol, monkeypatch, answers):
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, **answers)
    assert type(stop.value).__name__ == "AuditStop"
    assert ARCHIVE in str(stop.value) and C[:10] in str(stop.value)


def test_a_failed_archive_descent_read_stops_the_run_naming_it(ol, monkeypatch):
    # A pin, per the spec's list: a failed read is a stop, as every read's is.
    with pytest.raises(Exception) as stop:
        audit_with(ol, monkeypatch, **{"archive-descent": FAILED})
    assert type(stop.value).__name__ == "AuditStop"
    assert "merge-base" in str(stop.value) and "exit 128" in str(stop.value)
    assert C in str(stop.value)


LANE_CASES = {
    "claimed lane, unmarked commit": (
        marked(CLAIM),
        [(X, marked("lane work")), (Y, "unmarked lane work")],
        Y[:10],
        2,
    ),
    "telemetry marks the lane from that commit on": (
        CLAIM,
        [
            (X, "a person's work"),
            (T, marked("telemetry: session wi-1 s")),
            (Y, "unmarked"),
        ],
        Y[:10],
        2,
    ),
    "telemetry mark, the person's earlier commit exempt": (
        CLAIM,
        [(X, "a person's work"), (T, marked("telemetry: session wi-1 s"))],
        None,
        1,
    ),
    "another run's well-formed session passes": (
        marked(CLAIM, OTHER),
        [(X, marked("lane work", OTHER))],
        None,
        1,
    ),
    "a person's lane passes": (CLAIM, [(X, "a person's work")], None, None),
    "a re-claim closes the window": (
        marked(CLAIM),
        [(X, RECLAIM, EMPTY), (Y, "unmarked lane work")],
        None,
        0,
    ),
    "a re-claim that changes the tree is refused": (
        marked(CLAIM),
        [(X, RECLAIM), (Y, "unmarked lane work")],
        X[:10],
        2,
    ),
}


@pytest.mark.parametrize("case", sorted(LANE_CASES))
def test_the_lane_rule_is_the_merge_slots(ol, monkeypatch, case):
    claim, commits, named, window = LANE_CASES[case]
    fake = FakeGit(lane=ok(lane_log(*commits)), claim=ok(records((B, claim))))
    monkeypatch.setattr(ol, "run_git", fake, raising=False)
    refusal, size = ol.lane_refusal("repo", "wi-1", B)
    assert size == window
    if named is None:
        assert refusal is None
    else:
        assert named in refusal and "Loop-Session" in refusal


# --- the block, the skill section and the recipes hold to one another ---------
SKILL_DIR = KIT / "skills" / "coordinator-cycle"


def sections(text):
    """{number: body} for each `## N. Title` section of a markdown file."""
    parts = re.split(r"^## (\d+)\. ", text, flags=re.M)
    return {int(n): body for n, body in zip(parts[1::2], parts[2::2])}


def test_the_block_opens_with_the_marker_check_and_the_skill_section_links_it():
    block = BLOCK.read_text(encoding="utf-8")
    assert 'echo "$KIT_LOOP_SESSION"' in block.strip().splitlines()[0]
    assert "coordinator-cycle" in block and 'section 7, "Headless legs"' in block
    skill = sections((SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))
    assert skill[7].startswith("Headless legs\n")
    link = "../../../scripts/coordinator/headless-leg.md"
    assert "]({})".format(link) in skill[7]
    assert (SKILL_DIR / link).resolve() == BLOCK.resolve()
    recipes = sections(
        (SKILL_DIR / "references" / "recipes.md").read_text(encoding="utf-8")
    )
    for number in (1, 3, 7):
        assert "SKILL §7" in recipes[number], number
