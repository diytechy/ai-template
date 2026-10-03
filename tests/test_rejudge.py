"""rejudge.py — the checkpoint re-judge decision (TC-247), and the release
checkpoint that files it (TC-248's release half; its merge half is in
`tests/test_intake.py`).

An observation test case is one recorded as not automated: a judgment the
harness cannot rerun. Its latest result carries a digest of the inputs it
judged and an expiry. At a work-item merge and at release preparation, each
such case whose declared inputs no longer hash to that digest, whose result
expired, or which has no result, is due, and gets exactly one open re-judge
work item. The check hashes files; it runs no model.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: every case builds and
commits a real git repository, because the decision reads the inputs at a
revision, and the release half drives the intake mint's bookkeeping commit.
"""

import datetime
import csv
import io
import os
import subprocess

import pytest
from conftest import (
    SCRIPTS,
    env_gate_skipif,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

pytestmark = env_gate_skipif("git")

rejudge = load_script("rejudge")
intake = load_script("intake")
record_observation = load_script("record_observation")
adjudicate_brief = load_script("adjudicate_brief")
acommon = load_script("agent_common")
import kitlib.observation as OBS  # noqa: E402  (scripts/ is on the path by now)

UTC = datetime.timezone.utc
# The decision is handed its instant; the brief's live re-derivation reads the
# clock, so the fixtures' records are dated from the real one.
NOW = datetime.datetime.now(UTC).replace(microsecond=0)

TC_CSV = "docs/test/test-cases.csv"
# An automated case (never an observation), two observation cases declaring
# what they read and a thirty-day lifetime, one observation case declaring no
# inputs, and the template's `-000` example, which is nobody's case.
TEST_CASES = (
    "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,"
    "Inputs,MaxAge\n"
    "TC-000,SR-001,Inspection,the example,Release,x,No,docs/m.md,Drafted,"
    "src/a.txt,30\n"
    "TC-001,SR-001,Unit,call add,Smoke,x,Yes,tests/t.py,Approved,,\n"
    "TC-002,SR-001,Inspection,a reader reads the page,Release,"
    "the page reads,No,docs/m.md,Approved,src/a.txt;src/b.txt,30\n"
    "TC-003,SR-001,Inspection,a reader reads the other page,Release,"
    "the other page reads,No,docs/m.md,Approved,src/c.txt,30\n"
    "TC-004,SR-001,Demonstration,an adopter's first week,Release,"
    "the week goes well,No,docs/m.md,Approved,,30\n"
)


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message):
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD").strip()


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def spec_text(wid, title, **frontmatter):
    lines = ['id = "{}"'.format(wid), 'title = "{}"'.format(title)]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(
                "{} = [{}]".format(key, ", ".join('"{}"'.format(v) for v in value))
            )
        else:
            lines.append('{} = "{}"'.format(key, value))
    return "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"


def write_spec(root, where, wid, title, slug="thing", **frontmatter):
    return _write(
        root,
        "{}/{}-{}.md".format(where, wid, slug),
        spec_text(wid, title, **frontmatter),
    )


def git_repo(tmp_path):
    """A committed repository holding the test-case registry, three declared
    inputs and one queued work item; no observation record yet."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    _write(root, "docs/stack.ini", "[generated]\nPROJECT_STATE.html = trajectory\n")
    trace = load_script("trace")
    _write(
        root,
        trace.WATERMARK,
        trace.render_watermark({s: 0 for s in trace.WATERMARK_SPACES}),
    )
    _write(root, "seed.txt", "seed\n")
    _write(root, "src/a.txt", "a, as judged\n")
    _write(root, "src/b.txt", "b, as judged\n")
    _write(root, "src/c.txt", "c, as judged\n")
    # Digest-focused legacy fixtures disable cadence; cadence tests set 2.
    _write(root, "docs/process.toml", "[checks]\nobservation_min_work_items = 0\n")
    _write(root, TC_CSV, TEST_CASES)
    write_spec(root, "docs/work/queued", "WI-001", "Some unrelated work")
    _commit(root, "seed")
    return root


def _utc(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def record(root, tc, *, observed, expires, inputs=None, judged=None, outcome="pass"):
    """Write one observation record the way the writer does, judging the
    case's declared inputs as they stand in the working tree now."""
    if judged is None:
        judged = record_observation.inputs_digest(root, inputs or [])
    rec = {
        "tc": tc,
        "outcome": outcome,
        "observed_at": _utc(observed),
        "provenance": "a reader",
        "expires": _utc(expires),
        "judged": judged,
    }
    path = root / OBS.OBSERVATIONS_DIR / OBS.record_name(tc, rec["observed_at"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(OBS.render(rec), encoding="utf-8", newline="\n")
    return path


def judged_repo(tmp_path, *, expired=(), unrecorded=()):
    """The repository with a current record for each observation case, except
    the cases named `unrecorded` (no record) and `expired` (a record whose
    lifetime ran out before NOW); returns `(root, sha)`."""
    root = git_repo(tmp_path)
    inputs = {"TC-002": ["src/a.txt", "src/b.txt"], "TC-003": ["src/c.txt"]}
    for tc in ("TC-002", "TC-003", "TC-004"):
        if tc in unrecorded:
            continue
        if tc in expired:
            observed, expires = (
                NOW - datetime.timedelta(days=40),
                NOW - datetime.timedelta(days=10),
            )
        else:
            observed, expires = (
                NOW - datetime.timedelta(days=2),
                NOW + datetime.timedelta(days=28),
            )
        record(root, tc, observed=observed, expires=expires, inputs=inputs.get(tc))
    return root, _commit(root, "judged")


def cadence_repo(tmp_path, trigger="", floor=2, *, expired=(), unrecorded=()):
    root, _ = judged_repo(tmp_path, expired=expired, unrecorded=unrecorded)
    reader = csv.DictReader(io.StringIO(TEST_CASES))
    out = io.StringIO()
    writer = csv.DictWriter(
        out, fieldnames=[*reader.fieldnames, "Trigger", "MinWorkItems"]
    )
    writer.writeheader()
    for row in reader:
        if row["TC-ID"] == "TC-002":
            row.update(Trigger=trigger, MinWorkItems=floor)
        writer.writerow(row)
    _write(root, TC_CSV, out.getvalue())
    _write(root, "docs/process.toml", "[checks]\nobservation_min_work_items = 2\n")
    _write(
        root,
        "docs/requirements/low-level-requirements.toml",
        '[design.LLR-001]\nmodule = "src/a.txt"\ncomponent = "CMP-001"\n',
    )
    return root, _commit(root, "cadence policy")


def close_work(root, number):
    write_spec(root, "docs/archive/work/complete", f"WI-{number:03}", "closed work")
    return _commit(root, "closed work")


def case_due(root, sha, checkpoint="merge"):
    return any(
        d["tc"] == "TC-002"
        for d in rejudge.due_cases(root, sha, NOW, checkpoint=checkpoint)
    )


@pytest.mark.parametrize(
    "trigger,checkpoint,path",
    [
        ("files:src/*.txt", "merge", "src/b.txt"),
        ("component:CMP-001", "merge", "src/a.txt"),
        ("release", "release", None),
        ("stage-gate", "stage-gate", None),
        ("", "merge", "src/b.txt"),
    ],
)
def test_trigger_waits_for_closed_work_floor(tmp_path, trigger, checkpoint, path):
    root, _ = cadence_repo(tmp_path, trigger)
    if path:
        _write(root, path, "trigger moved\n")
    sha = close_work(root, 10)
    assert not case_due(root, sha, checkpoint)
    sha = close_work(root, 11)
    assert case_due(root, sha, checkpoint)
    assert rejudge.checkpoint_drafts(root, sha, checkpoint, now=NOW)


@pytest.mark.parametrize(
    "trigger,checkpoint,path",
    [
        ("files:other/*.txt", "merge", "src/b.txt"),
        ("component:CMP-001", "merge", "src/b.txt"),
        ("release", "merge", "src/a.txt"),
        ("stage-gate", "release", "src/a.txt"),
        ("", "merge", "other/a.txt"),
    ],
)
def test_floor_alone_does_not_fire_trigger(tmp_path, trigger, checkpoint, path):
    root, _ = cadence_repo(tmp_path, trigger)
    _write(root, path, "unrelated\n")
    close_work(root, 10)
    sha = close_work(root, 11)
    assert not case_due(root, sha, checkpoint)


def test_case_floor_can_raise_but_not_lower_default(tmp_path):
    root, _ = cadence_repo(tmp_path, "files:src/*", floor=1)
    _write(root, "src/a.txt", "changed\n")
    sha = close_work(root, 10)
    assert not case_due(root, sha)
    sha = close_work(root, 11)
    assert case_due(root, sha)


def test_raised_floor_and_bookkeeping_do_not_count(tmp_path):
    root, _ = cadence_repo(tmp_path, "files:src/*", floor=3)
    _write(root, "src/a.txt", "changed\n")
    close_work(root, 10)
    close_work(root, 11)
    _write(root, "notes.txt", "bookkeeping\n")
    sha = _commit(root, "mint: WI-012")
    assert not case_due(root, sha)
    sha = close_work(root, 12)
    assert case_due(root, sha)


@pytest.mark.parametrize("state", ["expired", "unrecorded"])
def test_first_judgement_and_expiry_bypass_trigger_and_floor(tmp_path, state):
    root, sha = cadence_repo(tmp_path, "release", **{state: ("TC-002",)})
    assert case_due(root, sha)


def test_trigger_reads_committed_revision_and_new_result_resets_floor(tmp_path):
    root, sha = cadence_repo(tmp_path, "files:src/*")
    close_work(root, 10)
    sha = close_work(root, 11)
    _write(root, "src/a.txt", "working tree only\n")
    assert not case_due(root, sha)

    sha = _commit(root, "trigger change")
    assert case_due(root, sha)
    record(
        root,
        "TC-002",
        observed=NOW,
        expires=NOW + datetime.timedelta(days=30),
        inputs=["src/a.txt", "src/b.txt"],
    )
    _commit(root, "fresh judgement")
    _write(root, "src/b.txt", "changed again\n")
    sha = close_work(root, 12)
    assert not case_due(root, sha)


def test_undeclared_process_policy_uses_ten_closed_work_items(tmp_path):
    root, _ = cadence_repo(tmp_path)
    (root / "docs/process.toml").unlink()
    _write(root, "src/b.txt", "changed\n")
    for number in range(10, 19):
        sha = close_work(root, number)
    assert not case_due(root, sha)
    sha = close_work(root, 19)
    assert case_due(root, sha)


def test_existing_archive_edits_do_not_count_as_new_closed_work(tmp_path):
    root, _ = cadence_repo(tmp_path, "release")
    close_work(root, 10)
    _write(
        root, "docs/archive/work/complete/WI-010-thing.md", "changed archive prose\n"
    )
    sha = _commit(root, "archive maintenance")
    assert not case_due(root, sha, "release")


def test_trajectory_rubric_warning_survives_strict_and_no_work_items(tmp_path):
    _write(tmp_path, TC_CSV, TEST_CASES)
    proc = run_py([SCRIPTS / "check_trajectory.py", "--strict"], tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" in proc.stderr and "TC-002" in proc.stderr and "Rubric" in proc.stderr


def test_release_trigger_rejudge_brief_still_composes(tmp_path):
    root, _ = cadence_repo(tmp_path, "release")
    close_work(root, 10)
    close_work(root, 11)
    values, refusal = adjudicate_brief.rejudge_values(root, {"Adjudicates": "TC-002"})
    assert refusal is None
    assert values["tc"] == "TC-002"


def test_component_trigger_matches_interface_owner_module_name(tmp_path):
    root, _ = cadence_repo(tmp_path, "component:CMP-002")
    _write(
        root,
        "docs/requirements/interfaces.toml",
        '[interface.IF-001]\nowner = "scripts/logic"\ncomponent = "CMP-002"\n',
    )
    _write(root, "project-trajectory/scripts/logic.py", "# component changed\n")
    close_work(root, 10)
    sha = close_work(root, 11)
    assert case_due(root, sha)


def drafts_by_case(drafts):
    out = {}
    for draft in drafts:
        (tc,) = draft["adjudicates"]
        assert tc not in out, "two drafts for {}".format(tc)
        out[tc] = draft
    return out


# --- TC-247: the decision -----------------------------------------------------


def test_the_observation_cases_are_read_at_the_revision(tmp_path):
    root, sha = judged_repo(tmp_path)
    ids = [r["TC-ID"] for r in rejudge.observation_test_cases(root, sha)]
    # Automated = No is the class; the automated case and the template's
    # example are not observation cases.
    assert ids == ["TC-002", "TC-003", "TC-004"]
    # ...and it is the registry AT that revision: a case added in the working
    # tree only is not read.
    _write(
        root,
        TC_CSV,
        TEST_CASES
        + "TC-005,SR-001,Inspection,new,Release,x,No,docs/m.md,Drafted,,30\n",
    )
    ids = [r["TC-ID"] for r in rejudge.observation_test_cases(root, sha)]
    assert "TC-005" not in ids


def test_an_unchanged_unexpired_case_gets_no_draft(tmp_path):
    root, sha = judged_repo(tmp_path)
    assert rejudge.checkpoint_drafts(root, sha, "merge", now=NOW) == []


def test_a_changed_input_gets_one_draft_naming_the_case_and_the_input(tmp_path):
    root, _ = judged_repo(tmp_path)
    _write(root, "src/b.txt", "b, CHANGED since it was judged\n")
    sha = _commit(root, "a merged change to one input")
    drafts = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    assert set(drafts) == {"TC-002"}
    draft = drafts["TC-002"]
    # The mint's typed cells: an adjudication row routed to the re-judge brief,
    # scoped to the one case.
    assert draft["kind"] == "adjudication"
    assert draft["brief"] == rejudge.BRIEF
    assert draft["adjudicates"] == ["TC-002"]
    # The title carries the case id and the digest prefix of what it reads now.
    now_digest = record_observation.inputs_digest(root, ["src/a.txt", "src/b.txt"])
    assert "TC-002" in draft["title"]
    assert now_digest[: len("sha256:") + rejudge.DIGEST_CHARS] in draft["title"]
    # It names what changed: the input that moved, and not the one that did not.
    assert "src/b.txt" in draft["context"]
    changed_line = [
        ln for ln in draft["context"].splitlines() if "changed" in ln.lower()
    ]
    assert changed_line and all("src/a.txt" not in ln for ln in changed_line)


def test_an_expired_result_gets_one_draft(tmp_path):
    root, sha = judged_repo(tmp_path, expired=("TC-003",))
    drafts = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "release", now=NOW))
    assert set(drafts) == {"TC-003"}
    assert "expired" in drafts["TC-003"]["context"]
    assert "release" in drafts["TC-003"]["title"]


def test_a_case_with_no_result_gets_one_draft(tmp_path):
    root, sha = judged_repo(tmp_path, unrecorded=("TC-002",))
    drafts = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    assert set(drafts) == {"TC-002"}
    assert "no result" in drafts["TC-002"]["context"]


def test_a_case_declaring_no_inputs_is_judged_by_expiry_and_absence_alone(tmp_path):
    # Current and unexpired: nothing, whatever else moves in the tree.
    root, _ = judged_repo(tmp_path)
    for rel in ("src/a.txt", "src/b.txt", "src/c.txt", "seed.txt"):
        _write(root, rel, "everything moved\n")
    sha = _commit(root, "every file moved")
    assert "TC-004" not in drafts_by_case(
        rejudge.checkpoint_drafts(root, sha, "merge", now=NOW)
    )
    # Expired: one. Absent: one.
    root, sha = judged_repo(tmp_path / "expired", expired=("TC-004",))
    assert set(
        drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    ) == {"TC-004"}
    root, sha = judged_repo(tmp_path / "absent", unrecorded=("TC-004",))
    drafts = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    assert set(drafts) == {"TC-004"}
    assert "no inputs" in drafts["TC-004"]["title"]


def test_inputs_are_read_at_the_revision_not_the_working_tree(tmp_path):
    root, sha = judged_repo(tmp_path)
    # An uncommitted edit to an input changes nothing at a committed revision.
    _write(root, "src/a.txt", "an uncommitted edit\n")
    _write(root, "src/c.txt", "another uncommitted edit\n")
    assert rejudge.checkpoint_drafts(root, sha, "merge", now=NOW) == []
    # ...and the same edit, committed, is due.
    sha2 = _commit(root, "the edits land")
    assert set(
        drafts_by_case(rejudge.checkpoint_drafts(root, sha2, "merge", now=NOW))
    ) == {
        "TC-002",
        "TC-003",
    }


def test_an_open_item_found_by_its_typed_cells_suppresses_a_second_draft(tmp_path):
    root, sha = judged_repo(tmp_path, unrecorded=("TC-002", "TC-003"))
    first = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    title = first["TC-002"]["title"]
    # An OPEN re-judge item for TC-002, found by its typed cells: no draft.
    write_spec(
        root,
        "docs/work/queued",
        "WI-002",
        "whatever its title says",
        slug="rejudge",
        safety_class="adjudication",
        brief=rejudge.BRIEF,
        adjudicates=["TC-002"],
    )
    # A CLOSED re-judge item for TC-003 with the identical title the next draft
    # would carry, in the archive: it suppresses nothing.
    write_spec(
        root,
        "docs/archive/work/complete",
        "WI-003",
        first["TC-003"]["title"],
        slug="rejudged",
        safety_class="adjudication",
        brief=rejudge.BRIEF,
        adjudicates=["TC-003"],
    )
    # An open row carrying TC-002's identical title but none of the typed
    # cells is not a re-judge item: the match is never by title.
    write_spec(root, "docs/work/queued", "WI-004", title, slug="lookalike")
    rows = acommon.read_spec_rows(root / "docs" / "work")
    assert rejudge._open_rejudge(rows, "TC-002")["WI-ID"] == "WI-002"
    assert rejudge._open_rejudge(rows, "TC-003") is None
    again = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    assert set(again) == {"TC-003"}
    # With only the lookalike open, TC-002 is drafted again.
    (root / "docs/work/queued/WI-002-rejudge.md").unlink()
    rows = acommon.read_spec_rows(root / "docs" / "work")
    assert rejudge._open_rejudge(rows, "TC-002") is None
    assert "TC-002" in drafts_by_case(
        rejudge.checkpoint_drafts(root, sha, "merge", now=NOW)
    )


def test_no_agent_command_is_spawned(tmp_path, monkeypatch):
    root, _ = judged_repo(tmp_path, expired=("TC-003",), unrecorded=("TC-004",))
    _write(root, "src/a.txt", "moved\n")
    sha = _commit(root, "moved")
    spawned = []
    real_popen = subprocess.Popen

    class Recording(real_popen):
        def __init__(self, args, *rest, **kw):
            spawned.append(args if isinstance(args, str) else list(args))
            super().__init__(args, *rest, **kw)

    monkeypatch.setattr(subprocess, "Popen", Recording)
    drafts = rejudge.checkpoint_drafts(root, sha, "merge", now=NOW)
    assert len(drafts) == 3
    assert spawned, "the decision read nothing from git - the probe is vacuous"
    for argv in spawned:
        head = argv if isinstance(argv, str) else os.path.basename(str(argv[0]))
        assert str(head).lower().startswith("git"), argv


# --- TC-248: the release checkpoint -------------------------------------------


def _queued_rejudges(root):
    return [
        r
        for r in acommon.read_spec_rows(root / "docs" / "work")
        if r["Status"] == "queued" and r.get("Brief") == rejudge.BRIEF
    ]


def test_the_release_subcommand_mints_for_an_expired_result_once(tmp_path, capsys):
    root = git_repo(tmp_path)
    now = datetime.datetime.now(UTC).replace(microsecond=0)
    inputs = {"TC-002": ["src/a.txt", "src/b.txt"], "TC-003": ["src/c.txt"]}
    for tc in ("TC-002", "TC-003", "TC-004"):
        if tc == "TC-003":
            observed, expires = (
                now - datetime.timedelta(days=40),
                now - datetime.timedelta(days=10),
            )
        else:
            observed, expires = (
                now - datetime.timedelta(days=1),
                now + datetime.timedelta(days=20),
            )
        record(root, tc, observed=observed, expires=expires, inputs=inputs.get(tc))
    _commit(root, "judged")
    # An unrelated uncommitted edit in the checkout, outside the mint's scope.
    _write(root, "seed.txt", "the owner's uncommitted edit\n")
    code = intake.main(["--root", str(root), "rejudge", "--checkpoint", "release"])
    assert code == 0, capsys.readouterr()
    minted = _queued_rejudges(root)
    assert [r["Adjudicates"] for r in minted] == ["TC-003"]
    assert minted[0]["SafetyClass"] == "adjudication"
    # The mint is a trunk commit, and it did not sweep in or discard the edit.
    assert (root / "seed.txt").read_text(encoding="utf-8") == (
        "the owner's uncommitted edit\n"
    )
    assert "seed.txt" in _git(root, "status", "--porcelain")
    assert "seed.txt" not in _git(root, "show", "--name-only", "--format=", "HEAD")
    # A second release preparation while that item is open files nothing.
    code = intake.main(["--root", str(root), "rejudge", "--checkpoint", "release"])
    assert code == 0, capsys.readouterr()
    assert len(_queued_rejudges(root)) == 1


def test_the_release_checklist_carries_the_required_rejudge_item(tmp_path):
    root = git_repo(tmp_path)
    now = datetime.datetime.now(UTC).replace(microsecond=0)
    # TC-003 expired, TC-004 never judged, TC-002 current: two due.
    record(
        root,
        "TC-002",
        observed=now - datetime.timedelta(days=1),
        expires=now + datetime.timedelta(days=20),
        inputs=["src/a.txt", "src/b.txt"],
    )
    record(
        root,
        "TC-003",
        observed=now - datetime.timedelta(days=40),
        expires=now - datetime.timedelta(days=10),
        inputs=["src/c.txt"],
    )
    _commit(root, "judged")
    out = root / "checklist.md"
    proc = run_py(
        [SCRIPTS / "gen_release_checklist.py", "--docs", root / "docs", "--out", out],
        cwd=root,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = out.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if "rejudge --checkpoint release" in ln]
    assert len(lines) == 1, text
    assert lines[0].startswith("- [ ] **Required")
    assert "2 observation test case" in lines[0]
    assert "intake.py rejudge --checkpoint release" in lines[0]


def test_a_minted_rejudge_row_composes_its_brief_and_demands_its_verdict(tmp_path):
    """The kind the draft declares requires a routed brief: an adjudication row
    declaring a brief the kit cannot compose is held for a human, so the
    re-judge brief is filled from the live decision and ends in a typed
    verdict line."""
    root, _ = judged_repo(tmp_path, expired=("TC-003",))
    row = {"WI-ID": "WI-009", "Brief": rejudge.BRIEF, "Adjudicates": "TC-003"}
    text, why = adjudicate_brief.compose(root, row, root / "verdict.md")
    assert why is None, why
    assert "TC-003" in text and "a reader reads the other page" in text
    assert "record_observation.py --tc TC-003" in text
    assert "expired" in text
    verdict = root / "verdict.md"
    verdict.write_text("OUTCOME: RECORDED result=pass\n", encoding="utf-8")
    assert adjudicate_brief.verdict_refusal(rejudge.BRIEF, verdict) is None
    verdict.write_text("OUTCOME: RECORDED\n", encoding="utf-8")
    assert "result" in adjudicate_brief.verdict_refusal(rejudge.BRIEF, verdict)
    # A case no longer due refuses: there is nothing left to judge.
    row["Adjudicates"] = "TC-002"
    text, why = adjudicate_brief.compose(root, row, verdict)
    assert text is None and "no longer due" in why


@pytest.mark.parametrize("checkpoint", ["phase-close", ""])
def test_an_undeclared_checkpoint_is_refused(tmp_path, checkpoint):
    root, sha = judged_repo(tmp_path)
    with pytest.raises(ValueError):
        rejudge.checkpoint_drafts(root, sha, checkpoint, now=NOW)


# --- review follow-up: inputs outside the repository are never read ----------


def _escape_repo(tmp_path, outside):
    """A repo whose one observation case declares an in-repo input beside
    `outside`, a name that points out of the repository."""
    root = git_repo(tmp_path)
    _write(
        root,
        TC_CSV,
        "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,"
        "Inputs,MaxAge\n"
        "TC-002,SR-001,Inspection,a reader reads,Release,it reads,No,docs/m.md,"
        "Approved,src/a.txt;{},30\n".format(outside),
    )
    return root


@pytest.mark.parametrize("style", ["posix-dotdot", "windows-dotdot", "absolute"])
def test_an_input_outside_the_repository_is_never_hashed(tmp_path, style):
    """Only committed bytes are hashed: a declared input naming a file outside
    the repository, in either path style, digests as a fixed token and never
    as the file's content, so editing that file moves nothing."""
    target = tmp_path / "outside.txt"
    target.write_text("outside, as judged\n", encoding="utf-8")
    name = {
        "posix-dotdot": "../outside.txt",
        "windows-dotdot": r"..\outside.txt",
        "absolute": target.as_posix(),
    }[style]
    root = _escape_repo(tmp_path, name)
    before = record_observation.inputs_digest(root, [name])
    target.write_text("outside, EDITED\n", encoding="utf-8")
    assert record_observation.inputs_digest(root, [name]) == before
    # The writer refuses the case, naming the input, and writes nothing.
    with pytest.raises(SystemExit) as refused:
        record_observation.build_observation(root, "TC-002", "pass", "a reader")
    assert name in str(refused.value)
    # A checkpoint judges committed bytes only: a record judged before the
    # outside file moved is still current after it moved.
    record(
        root,
        "TC-002",
        observed=NOW - datetime.timedelta(days=1),
        expires=NOW + datetime.timedelta(days=20),
        inputs=["src/a.txt", name],
    )
    sha = _commit(root, "judged")
    target.write_text("outside, EDITED AGAIN\n", encoding="utf-8")
    assert rejudge.checkpoint_drafts(root, sha, "merge", now=NOW) == []


# --- review follow-up: one snapshot per revision ------------------------------

MANY = 12


def _many_repo(tmp_path):
    """MANY observation cases of four inputs each, all judged in one commit,
    then every input changed in the next: `(root, sha)`."""
    root = git_repo(tmp_path)
    rows = [
        "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,"
        "Inputs,MaxAge"
    ]
    inputs = {}
    for i in range(1, MANY + 1):
        tc = "TC-{:03d}".format(100 + i)
        inputs[tc] = ["src/case{}/in{}.txt".format(i, k) for k in range(4)]
        for rel in inputs[tc]:
            _write(root, rel, "as judged\n")
        rows.append(
            "{},SR-001,Inspection,read {},Release,x,No,docs/m.md,Approved,{},30".format(
                tc, i, ";".join(inputs[tc])
            )
        )
    _write(root, TC_CSV, "\n".join(rows) + "\n")
    for tc, names in inputs.items():
        record(
            root,
            tc,
            observed=NOW - datetime.timedelta(days=1),
            expires=NOW + datetime.timedelta(days=20),
            inputs=names,
        )
    _commit(root, "judged")
    for names in inputs.values():
        _write(root, names[1], "changed\n")
    return root, _commit(root, "every case's second input changed")


def test_one_snapshot_per_revision_whatever_the_case_count(tmp_path, monkeypatch):
    root, sha = _many_repo(tmp_path)
    snapshots = []
    real = rejudge._extract

    def counting(root_, sha_, paths, dest):
        snapshots.append(sha_)
        return real(root_, sha_, paths, dest)

    monkeypatch.setattr(rejudge, "_extract", counting)
    drafts = drafts_by_case(rejudge.checkpoint_drafts(root, sha, "merge", now=NOW))
    assert len(drafts) == MANY
    for i, (tc, draft) in enumerate(sorted(drafts.items()), start=1):
        assert "src/case{}/in1.txt".format(i) in draft["context"], tc
        assert (
            "src/case{}/in0.txt;".format(i)
            not in draft["context"].split("What changed")[1].splitlines()[0]
        )
    # The checkpoint's revision and the one revision every result was judged
    # at: two snapshots, not one per case or per input.
    assert len(snapshots) == 2
    assert len(set(snapshots)) == 2


def test_the_pathspec_is_chunked_and_the_answer_is_unchanged(tmp_path, monkeypatch):
    root, sha = _many_repo(tmp_path)
    whole = rejudge.checkpoint_drafts(root, sha, "merge", now=NOW)
    archives = []
    real = rejudge._archive_chunk

    def counting(root_, sha_, chunk, dest):
        archives.append(len(chunk))
        return real(root_, sha_, chunk, dest)

    monkeypatch.setattr(rejudge, "PATHSPEC_CHUNK", 5)
    monkeypatch.setattr(rejudge, "_archive_chunk", counting)
    assert rejudge.checkpoint_drafts(root, sha, "merge", now=NOW) == whole
    assert archives and max(archives) <= 5
    assert len(archives) > 2


# --- review follow-up: the CLI is the release entry only ---------------------


def test_the_cli_refuses_a_manual_merge_checkpoint(tmp_path, capsys):
    root, _ = judged_repo(tmp_path, unrecorded=("TC-002",))
    with pytest.raises(SystemExit) as refused:
        intake.main(["--root", str(root), "rejudge", "--checkpoint", "merge"])
    assert refused.value.code == 2
    assert _queued_rejudges(root) == []


# --- review follow-up: the mint path's checks and its staging -----------------


def test_the_release_mint_runs_the_mint_checks(tmp_path, monkeypatch):
    root, _ = judged_repo(tmp_path, expired=("TC-003",))
    head = _git(root, "rev-parse", "HEAD").strip()
    seen = []

    def sentinel(drafts, subject_verb, registry, bodies):
        seen.append([d["title"] for d in drafts])
        return "SENTINEL mint-check refusal"

    monkeypatch.setattr(intake, "_pre_mint_refusal", sentinel)
    minted, refusal = intake.mint_rejudge(root, "HEAD", "release")
    assert (minted, refusal) == ([], "SENTINEL mint-check refusal")
    assert len(seen) == 1 and any("TC-003" in t for t in seen[0])
    assert _git(root, "rev-parse", "HEAD").strip() == head
    assert _queued_rejudges(root) == []


def test_a_pre_staged_unrelated_edit_survives_the_release_mint(tmp_path, capsys):
    root, _ = judged_repo(tmp_path, expired=("TC-003",))
    _write(root, "seed.txt", "the owner's STAGED edit\n")
    _git(root, "add", "seed.txt")
    _write(root, "src/c.txt", "an unstaged edit to an input\n")
    index = _git(root, "diff", "--cached", "--binary", "HEAD", "--", "seed.txt")
    staged = _git(root, "ls-files", "-s", "--", "seed.txt", "src/c.txt")
    worktree = {rel: (root / rel).read_bytes() for rel in ("seed.txt", "src/c.txt")}
    code = intake.main(["--root", str(root), "rejudge", "--checkpoint", "release"])
    assert code == 0, capsys.readouterr()
    assert [r["Adjudicates"] for r in _queued_rejudges(root)] == ["TC-003"]
    assert _git(root, "diff", "--cached", "--binary", "HEAD", "--", "seed.txt") == index
    assert _git(root, "ls-files", "-s", "--", "seed.txt", "src/c.txt") == staged
    assert {rel: (root / rel).read_bytes() for rel in worktree} == worktree
    # ...and the mint's own commit carries neither edit.
    shown = _git(root, "show", "--name-only", "--format=", "HEAD")
    assert "seed.txt" not in shown and "src/c.txt" not in shown


# --- review follow-up, second round: symlinks, `..` inside, one extraction ----


def _commit_symlink(root, rel, target):
    """Commit `rel` as a symbolic link to `target` straight into the index, so
    the commit holds a link whatever this platform can create on disk."""
    blob = subprocess.run(
        ["git", "-C", str(root), "hash-object", "-w", "--stdin"],
        input=target,
        capture_output=True,
        encoding="utf-8",
    ).stdout.strip()
    _git(root, "update-index", "--add", "--cacheinfo", "120000,{},{}".format(blob, rel))
    _git(root, "commit", "-qm", "link {}".format(rel))
    # Check the link out, so a later `add -A` keeps it rather than staging its
    # deletion (a platform without links writes it as a file of its target).
    _git(root, "checkout", "--", rel)
    return _git(root, "rev-parse", "HEAD").strip()


@pytest.mark.parametrize("style", ["absolute", "relative"])
def test_a_committed_symlink_leaving_the_repository_is_never_read(tmp_path, style):
    """A committed link whose target lies outside the repository is a link
    like any other, excluded from the digest: its target is never read, so
    editing that target moves nothing, and the checkpoint neither refuses nor
    follows it."""
    target = tmp_path / "outside.txt"
    target.write_text("outside, as judged\n", encoding="utf-8")
    root = _escape_repo(tmp_path, "docs/link.txt")
    _commit(root, "the case reads a link")
    link = target.as_posix() if style == "absolute" else "../../outside.txt"
    sha = _commit_symlink(root, "docs/link.txt", link)
    (due,) = rejudge.due_cases(root, sha, NOW)
    assert (due["tc"], due["why"]) == ("TC-002", rejudge.WHY_NEVER)
    target.write_text("outside, EDITED\n", encoding="utf-8")
    (again,) = rejudge.due_cases(root, sha, NOW)
    assert again["digest"] == due["digest"]


def test_a_checked_out_symlink_leaving_the_repository_is_never_read(tmp_path):
    """The writer's half: a link in the checkout whose target lies outside the
    repository is recorded without being read, as a declared input and inside
    a declared directory."""
    target = tmp_path / "outside.txt"
    target.write_text("outside, as judged\n", encoding="utf-8")
    root = git_repo(tmp_path)
    try:
        os.symlink(target, root / "src" / "link.txt")
    except OSError as exc:  # Windows without the symlink privilege
        pytest.skip("this platform cannot create a symlink: {}".format(exc))
    before = record_observation.inputs_digest(root, ["src/link.txt", "src"])
    target.write_text("outside, EDITED\n", encoding="utf-8")
    assert record_observation.inputs_digest(root, ["src/link.txt", "src"]) == before
    assert record_observation.inputs_digest(
        root, ["src/link.txt"]
    ) != record_observation.inputs_digest(root, ["src/absent.txt"])


def test_a_dotdot_that_stays_inside_is_read_as_its_normal_path(tmp_path):
    """`docs/../src/a.txt` names `src/a.txt`: the checkpoint digests the same
    committed file the writer judged, and a committed change to it is due."""
    root = git_repo(tmp_path)
    name = "docs/../src/a.txt"
    _write(
        root,
        TC_CSV,
        "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,"
        "Inputs,MaxAge\n"
        "TC-002,SR-001,Inspection,a reader reads,Release,it reads,No,docs/m.md,"
        "Approved,{},30\n".format(name),
    )
    assert record_observation.inputs_digest(
        root, [name]
    ) != record_observation.inputs_digest(root, ["docs/../src/absent.txt"])
    record(
        root,
        "TC-002",
        observed=NOW - datetime.timedelta(days=1),
        expires=NOW + datetime.timedelta(days=20),
        inputs=[name],
    )
    sha = _commit(root, "judged")
    assert rejudge.due_cases(root, sha, NOW) == []
    _write(root, "src/a.txt", "a, CHANGED\n")
    sha = _commit(root, "the input moved")
    (due,) = rejudge.due_cases(root, sha, NOW)
    assert (due["tc"], due["why"], due["changed"]) == (
        "TC-002",
        rejudge.WHY_CHANGED,
        [name],
    )


def test_a_result_judged_at_the_checkpoint_reuses_its_snapshot(tmp_path, monkeypatch):
    """A record committed in the checkpoint's own commit, judged against edits
    that commit does not hold, is due with every input named, and the
    checkpoint's revision is extracted once, not again as the result's."""
    root = git_repo(tmp_path)
    record(
        root,
        "TC-002",
        observed=NOW - datetime.timedelta(days=1),
        expires=NOW + datetime.timedelta(days=20),
        judged="sha256:" + "0" * 64,
    )
    for tc, inputs in (("TC-003", ["src/c.txt"]), ("TC-004", None)):
        record(
            root,
            tc,
            observed=NOW - datetime.timedelta(days=1),
            expires=NOW + datetime.timedelta(days=20),
            inputs=inputs,
        )
    sha = _commit(root, "judged, one against uncommitted edits")
    snapshots = []
    real = rejudge._extract

    def counting(root_, sha_, paths, dest):
        snapshots.append(sha_)
        return real(root_, sha_, paths, dest)

    monkeypatch.setattr(rejudge, "_extract", counting)
    (due,) = rejudge.due_cases(root, sha, NOW)
    assert (due["tc"], due["why"]) == ("TC-002", rejudge.WHY_CHANGED)
    assert due["changed"] == ["src/a.txt", "src/b.txt"]
    assert snapshots == [sha]


def _record_through_the_writer(root, tc):
    """Record a passing result for `tc` exactly as `record_observation.py`
    does, digesting the checkout as it stands."""
    rec = record_observation.build_observation(root, tc, "pass", "a reader")
    path = root / OBS.OBSERVATIONS_DIR / OBS.record_name(tc, rec["observed_at"])
    path.parent.mkdir(parents=True, exist_ok=True)
    OBS.write_atomic(path, OBS.render(rec))


def _linked_repo(tmp_path, declared, link, target):
    """A repository whose one case declares `declared`, holding the committed
    link `link` to `target`, built as a git blob so the platform need not be
    able to create one."""
    root = git_repo(tmp_path)
    _write(root, "src/target.txt", "the target, as judged\n")
    _write(root, "lnk/plain.txt", "a plain file beside the link\n")
    _write(
        root,
        TC_CSV,
        "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,"
        "Inputs,MaxAge\n"
        "TC-002,SR-001,Inspection,a reader reads,Release,it reads,No,docs/m.md,"
        "Approved,{},30\n".format(declared),
    )
    _commit(root, "the case")
    _commit_symlink(root, link, target)
    return root


@pytest.mark.parametrize("declared", ["lnk/link.txt", "lnk"])
def test_a_committed_link_is_not_content(tmp_path, declared):
    """A committed link is excluded from the digest, by the writer and the
    checkpoint alike: a result recorded through the writer is not due at the
    checkpoint, whatever this platform checked the link out as, and a change
    to the link's target does not make it due."""
    root = _linked_repo(tmp_path, declared, "lnk/link.txt", "../src/target.txt")
    _record_through_the_writer(root, "TC-002")
    sha = _commit(root, "judged through the writer")
    assert rejudge.due_cases(root, sha, NOW) == []
    _write(root, "src/target.txt", "the target, CHANGED\n")
    sha = _commit(root, "the target moved, the link did not")
    assert rejudge.due_cases(root, sha, NOW) == []


def test_a_directory_link_to_itself_is_harmless(tmp_path):
    """`lnk/self -> .` names the directory holding it: it is excluded like any
    link, so neither side walks into it and the checkpoint copies nothing."""
    root = _linked_repo(tmp_path, "lnk", "lnk/self", ".")
    _record_through_the_writer(root, "TC-002")
    sha = _commit(root, "judged through the writer")
    assert rejudge.due_cases(root, sha, NOW) == []
    _write(root, "lnk/plain.txt", "the plain file, CHANGED\n")
    sha = _commit(root, "the plain file moved")
    (due,) = rejudge.due_cases(root, sha, NOW)
    assert (due["why"], due["changed"]) == (rejudge.WHY_CHANGED, ["lnk"])
