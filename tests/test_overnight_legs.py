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
import pytest
from conftest import KIT
from kitlib import provenance

from overnight_legs_fixtures import BLOCK, LOOP_SESSION_ENV, handoff_text, load_launcher

WELL_FORMED = "20260101T000000Z-abcdef"


@pytest.fixture
def ol(tmp_path, monkeypatch):
    """The launcher, logging under `tmp_path`, with `sys.path` restored."""
    monkeypatch.setattr(sys, "path", list(sys.path))
    module = load_launcher()
    monkeypatch.setattr(module, "LOGDIR", tmp_path / "logs")
    monkeypatch.setattr(module, "lease_holder", lambda repo: None)
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


def marked(subject, session=WELL_FORMED):
    return "{}\n\nLoop-Session: {}".format(subject, session)


def records(*commits):
    """`git log --format=%H%x00%B%x1e` output for `(sha, message)` pairs."""
    return "".join("{}\x00{}\n\x1e\n".format(sha, msg) for sha, msg in commits)


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
            "trunk": ok(records((B, marked("handoff: leg 1")))),
            "archive": ok(records((D, marked("archive record")))),
            "lane": ok(records((L, marked("lane work")))),
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
    trunk_ref, _snapshot = ol.pre_leg("repo")
    return ol.audit("repo", trunk_ref, pre, WELL_FORMED)


@pytest.mark.parametrize(
    "site, named",
    [
        ("name", "symbolic-ref"),
        ("snapshot", "for-each-ref"),
        ("descent", "merge-base"),
        ("trunk", "{}..{}".format(A, B)),
        ("archive", "{}..{}".format(C, D)),
        ("lane", "{}..refs/heads/wi-1".format(B)),
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
    ],
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
        ({"claim": FAILED}, "--grep"),
    ],
)
def test_check_lane_refuses_when_a_read_fails(ol, monkeypatch, capsys, answers, named):
    monkeypatch.setattr(ol, "run_git", FakeGit(**answers), raising=False)
    assert ol.check_lane("repo", "wi-1") == 3
    assert named in capsys.readouterr().out


@pytest.mark.parametrize(
    "pre, answers, named",
    [
        (PRE, {"trunk": ok(records((B, "unmarked trunk work")))}, B[:10]),
        (PRE, {"trunk": ok(records((B, marked("foreign", OTHER))))}, B[:10]),
        (PRE, {"descent": (1, "", "")}, A[:10]),
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
}


@pytest.mark.parametrize("case", sorted(LANE_CASES))
def test_the_lane_rule_is_the_merge_slots(ol, monkeypatch, case):
    claim, commits, named, window = LANE_CASES[case]
    fake = FakeGit(lane=ok(records(*commits)), claim=ok(records((B, claim))))
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
