"""Verifies SR-217 / LLR-257 (TC-250; TC-468 to TC-471, each tagged on its own
tests) — the test-first order, read from history.

Every case drives `check_test_first.py` over a REAL git repository built commit
by commit, which is why the module is registered in conftest.SLOW_MODULES: the
order under test exists only in commits, so no in-memory fixture can stand in
for it. Most cases call the module's functions in-process on those repositories;
the cases about what the harness reads back (the printed report, the exit code,
the plan listing) run the delivered commands as subprocesses.

Each `History` commit rewrites the three registries whole from the rows declared
so far, so a commit's diff is exactly the rows the case changed in it. An
acceptance is an ACT: `History.act` takes it with the producer itself,
`baseline_snapshot.copy_live`, as `intake.py snapshot` does, so the act ledger
entry and the record's copies are the ones a real act commits. The first act
seeds the record, which is the record's cut; `History.seed` takes that first
copy over a placeholder row, for a case whose dates must all be exact.

Implements: TC-250
"""

import shutil
import subprocess

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, skip_without_env_gates

SR_REG = "docs/requirements/system-requirements.toml"
LLR_REG = "docs/requirements/low-level-requirements.toml"
TC_REG = "docs/test/test-cases.toml"
TABLES = {SR_REG: "requirement", LLR_REG: "design", TC_REG: "test"}
RECORD = "docs/archive/last_accepted"
LEDGER = RECORD + "/acts.toml"
# The record's earlier spelling, which the reader never reads (D3).
EARLIER = "docs/archive/last_approved"

_SNAPSHOT = []


def _snapshot():
    """`baseline_snapshot`, loaded once: the act's producer."""
    if not _SNAPSHOT:
        _SNAPSHOT.append(load_script("baseline_snapshot"))
    return _SNAPSHOT[0]


@pytest.fixture
def ctf():
    return load_script("check_test_first")


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _cell(value):
    if isinstance(value, list):
        return "[{}]".format(", ".join('"{}"'.format(v) for v in value))
    return '"{}"'.format(value)


class History:
    """A repository on `main`, committed one step at a time."""

    def __init__(self, root):
        skip_without_env_gates("git")
        root.mkdir(parents=True, exist_ok=True)
        self.root = root
        _git(root, "init", "-q")
        pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
        _git(root, "config", "user.email", "t@example.com")
        _git(root, "config", "user.name", "T")
        _git(root, "config", "commit.gpgsign", "false")
        _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
        self.rows = {path: {} for path in TABLES}

    def sr(self, rid, status):
        self.rows[SR_REG][rid] = {"title": "requirement " + rid, "status": status}
        return self

    def llr(self, rid, sr, status="Accepted"):
        self.rows[LLR_REG][rid] = {"sr_refs": [sr], "status": status}
        return self

    def tc(self, rid, verifies, status):
        self.rows[TC_REG][rid] = {"verifies": verifies, "status": status}
        return self

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return self

    def _registries(self):
        # A registry with no rows is not written, so a case can keep one tier
        # under an older carrier while the others are TOML.
        for rel, table in TABLES.items():
            if not self.rows[rel]:
                continue
            lines = []
            for rid, cells in self.rows[rel].items():
                lines.append("[{}.{}]".format(table, rid))
                lines += ["{} = {}".format(k, _cell(v)) for k, v in cells.items()]
                lines.append("")
            self.write(rel, "\n".join(lines))

    def commit(self, message, registries=True):
        if registries:
            self._registries()
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-q", "--allow-empty", "-m", message)
        return _git(self.root, "rev-parse", "HEAD")

    def act(self, message, reaccepts=()):
        """An acceptance act, committed: the registries written, then the
        record copied and its ledger entry appended by `copy_live`. The first
        act seeds the record."""
        self._registries()
        _snapshot().copy_live(
            self.root,
            seed=not (self.root / RECORD).is_dir(),
            reaccepts=set(reaccepts) or None,
        )
        return self.commit(message, registries=False)

    def seed(self):
        """The record's first copy, over a placeholder row the readers skip, so
        every act after it is dated exactly."""
        self.sr("SR-000", "Drafted")
        return self.act("the record seeded")


def implements(*ids):
    """A source file whose one declaration line names `ids`."""
    return '"""A module.\n\nImplements: {}\n"""\n'.format(", ".join(ids))


def as_tuples(findings):
    return [(f.requirement, f.implementation, list(f.late)) for f in findings]


def as_unread(findings):
    return [
        (f.requirement, [(rid, at.commit) for rid, at in f.unread])
        for f in findings
        if f.unread
    ]


def _judge(ctf, root, start=None):
    return ctf.test_first_findings(root, src="src", start=start)


# --- clause: test cases accepted first produce nothing ------------------------


def test_test_cases_all_accepted_before_the_implementation_produce_nothing(
    tmp_path, ctf
):
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Accepted")
    h.act("requirement, one test case accepted")
    h.tc("TC-001", ["SR-001"], "Accepted")
    h.act("second test case accepted")
    h.write("src/app.py", implements("SR-001"))
    h.commit("implementation")
    assert _judge(ctf, h.root) == []


# --- clause: landing through the requirement or a design row, earlier wins ----


@pytest.mark.parametrize("first", ["SR-001", "LLR-001"])
def test_the_landing_is_the_earlier_of_a_requirement_line_and_a_design_row_line(
    tmp_path, ctf, first
):
    # The test case is accepted BETWEEN the two declaring commits, so the report
    # exists only if the landing is read at the earlier one, whichever id it
    # names; a landing read at the later line would put the acceptance first.
    later = "LLR-001" if first == "SR-001" else "SR-001"
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").llr("LLR-001", "SR-001")
    h.tc("TC-001", ["SR-001", "LLR-001"], "Drafted")
    h.act("chain drafted")
    landing = h.write("src/a.py", implements(first)).commit("first declaration")
    acceptance = h.tc("TC-001", ["SR-001", "LLR-001"], "Accepted").act("accept")
    h.write("src/b.py", implements(later)).commit("second declaration")
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", acceptance)])
    ]


def test_first_implementation_commits_reads_each_id_at_its_earliest_line(tmp_path, ctf):
    h = History(tmp_path / "repo")
    one = h.write("src/a.py", implements("SR-001")).commit("one", registries=False)
    two = h.write("src/b.py", implements("SR-001", "LLR-001")).commit(
        "two", registries=False
    )
    # A declaration outside the declared source surface, or in a file type the
    # back-link grammar does not read, is not code declaring an implementation.
    h.write("docs/notes.md", "Implements: SR-002\n")
    h.write("tests/test_a.py", implements("SR-003")).commit("elsewhere", False)
    found = ctf.first_implementation_commits(h.root, src="src")
    assert found["SR-001"] == one
    assert found["LLR-001"] == two
    assert "SR-002" not in found and "SR-003" not in found


# --- clause: two late test cases, both acceptance commits named -----------------


def _two_late(root):
    h = History(root)
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Drafted")
    h.act("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    one = h.tc("TC-001", ["SR-001"], "Accepted").act("accept TC-001")
    two = h.tc("TC-002", ["SR-001"], "Accepted").act("accept TC-002")
    return h, landing, one, two


def test_two_test_cases_accepted_after_the_landing_are_both_named(tmp_path, ctf):
    h, landing, one, two = _two_late(tmp_path / "repo")
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", one), ("TC-002", two)])
    ]


def test_the_printed_report_names_the_requirement_and_every_commit(tmp_path):
    h, landing, one, two = _two_late(tmp_path / "repo")
    proc = run_py(
        [SCRIPTS / "check_test_first.py", "--root", ".", "--src", "src"], cwd=h.root
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    lines = [ln for ln in proc.stdout.splitlines() if "SR-001" in ln]
    assert len(lines) == 1, proc.stdout
    for token in ("WARN", "TC-001", "TC-002", landing[:10], one[:10], two[:10]):
        assert token in lines[0], (token, lines[0])


# --- clause: accepting one while withdrawing another --------------------------


def test_a_commit_accepting_one_test_case_while_withdrawing_another_records_it(
    tmp_path, ctf
):
    # The accepted-status count is the same on both sides of the swap, which is
    # why an occurrence-count pickaxe over the registry would see no change here.
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Accepted")
    first = h.act("drafted and accepted")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    h.tc("TC-001", ["SR-001"], "Accepted").tc("TC-002", ["SR-001"], "Drafted")
    swap = h.act("accept TC-001, withdraw TC-002")
    assert ctf.record_acceptances(h.root).tests == {
        "TC-002": ctf.Acceptance(first, True),
        "TC-001": ctf.Acceptance(swap, True),
    }
    assert as_tuples(_judge(ctf, h.root)) == [("SR-001", landing, [("TC-001", swap)])]


def test_a_withdrawn_and_reaccepted_test_case_keeps_its_first_acceptance(tmp_path, ctf):
    # LLR-257 records each row's FIRST move into acceptance. Re-accepting after a
    # withdrawal is not that move, from the root or from a declared start.
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Accepted")
    first = h.act("test case accepted first")
    start = h.write("src/app.py", implements("SR-001")).commit("implementation")
    h.tc("TC-001", ["SR-001"], "Drafted").act("withdrawn")
    h.tc("TC-001", ["SR-001"], "Accepted").act("re-accepted")
    record = ctf.record_acceptances(h.root)
    assert record.tests == {"TC-001": ctf.Acceptance(first, True)}
    assert record.pairs == {("TC-001", "SR-001"): ctf.Acceptance(first, True)}
    assert _judge(ctf, h.root) == []
    assert _judge(ctf, h.root, start=start) == []


# --- clause: no implementation produces nothing ------------------------------


def test_a_requirement_with_no_implementation_produces_nothing(tmp_path, ctf):
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted")
    h.write("src/app.py", "# relates to SR-001, but declares nothing\n")
    h.act("drafted")
    h.tc("TC-001", ["SR-001"], "Accepted").act("accept")
    assert _judge(ctf, h.root) == []


# --- clause: a declared start scopes the requirements judged ----------------


def _two_requirements(root):
    """SR-001 accepted in the first act, SR-002 accepted after `start`; both
    implemented at `start`, both with a test case accepted after it."""
    h = History(root)
    h.seed()
    h.sr("SR-001", "Accepted").sr("SR-002", "Drafted")
    h.tc("TC-001", ["SR-001"], "Drafted").tc("TC-002", ["SR-002"], "Drafted")
    h.act("SR-001 accepted")
    start = h.write("src/app.py", implements("SR-001", "SR-002")).commit("impl")
    h.sr("SR-002", "Accepted").act("SR-002 accepted")
    h.tc("TC-001", ["SR-001"], "Accepted").tc("TC-002", ["SR-002"], "Accepted")
    late = h.act("both test cases accepted")
    return h, start, late


def test_a_declared_start_after_a_requirements_acceptance_excludes_it(tmp_path, ctf):
    h, start, late = _two_requirements(tmp_path / "repo")
    assert as_tuples(_judge(ctf, h.root, start=start)) == [
        ("SR-002", start, [("TC-002", late)])
    ]


def test_no_declared_start_judges_the_whole_history(tmp_path, ctf):
    h, start, late = _two_requirements(tmp_path / "repo")
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", start, [("TC-001", late)]),
        ("SR-002", start, [("TC-002", late)]),
    ]


def test_a_test_case_accepted_after_the_landing_but_before_the_start_is_reported(
    tmp_path, ctf
):
    # SR-217 scopes only the REQUIREMENT's acceptance to the start. A test case's
    # acceptance is its earliest accepting act over the whole record, so a
    # test case accepted after the code landed stays late even when both
    # happened before the start the requirement was accepted after.
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Drafted").tc("TC-001", ["SR-001"], "Drafted").commit("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    acceptance = h.tc("TC-001", ["SR-001"], "Accepted").act("test case accepted")
    start = h.write("notes.txt", "adopted\n").commit("the rule adopted", False)
    h.sr("SR-001", "Accepted").act("requirement accepted after the start")
    assert as_tuples(_judge(ctf, h.root, start=start)) == [
        ("SR-001", landing, [("TC-001", acceptance)])
    ]


def test_the_start_is_read_from_the_declared_checks_key(tmp_path, ctf, capsys):
    h, start, _late = _two_requirements(tmp_path / "repo")
    h.write("docs/process.toml", '[checks]\ntest_first_since = "{}"\n'.format(start))
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    assert "SR-002" in out and "SR-001" not in out, out
    # An empty value declares no start, so the whole history is judged.
    h.write("docs/process.toml", '[checks]\ntest_first_since = ""\n')
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    assert "SR-001" in out and "SR-002" in out, out


# --- clause: a test case born accepted counts at its birth -------------------


def test_a_test_case_added_already_accepted_counts_at_its_birth(tmp_path, ctf):
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").act("requirement")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    born = h.tc("TC-001", ["SR-001"], "Accepted").act("test case, born accepted")
    assert ctf.record_acceptances(h.root).tests == {
        "TC-001": ctf.Acceptance(born, True)
    }
    assert as_tuples(_judge(ctf, h.root)) == [("SR-001", landing, [("TC-001", born)])]


# --- clause: a test case is the requirement's from its accepted-and-naming act -


def test_an_accepted_test_case_re_pointed_after_the_landing_is_dated_at_its_act(
    tmp_path, ctf
):
    # TC-001 was accepted long before SR-001's code, but for SR-002. Re-pointed
    # at SR-001 and re-accepted only after the code landed, it is SR-001's test
    # case from that act: its own earlier acceptance date does not travel.
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").sr("SR-002", "Accepted")
    h.tc("TC-001", ["SR-002"], "Accepted")
    early = h.act("TC-001 accepted for SR-002")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    h.tc("TC-001", ["SR-001"], "Accepted")
    repoint = h.act("TC-001 re-pointed and re-accepted", reaccepts=["TC-001"])
    assert ctf.record_acceptances(h.root).pairs == {
        ("TC-001", "SR-002"): ctf.Acceptance(early, True),
        ("TC-001", "SR-001"): ctf.Acceptance(repoint, True),
    }
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", repoint)])
    ]


def test_a_test_case_reaching_the_requirement_through_a_re_pointed_design_row(
    tmp_path, ctf
):
    # TC-001 names LLR-001 throughout and is accepted first. LLR-001 belonged to
    # SR-002 and is re-pointed at SR-001 after SR-001's code landed, so TC-001
    # names one of SR-001's design rows only from the act re-accepting it.
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").sr("SR-002", "Accepted").llr("LLR-001", "SR-002")
    h.tc("TC-001", ["LLR-001"], "Accepted").act("TC-001 accepted via LLR-001")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    h.llr("LLR-001", "SR-001")
    repoint = h.act("LLR-001 re-pointed at SR-001", reaccepts=["LLR-001"])
    assert ctf.record_acceptances(h.root).pairs[("TC-001", "SR-001")] == (
        ctf.Acceptance(repoint, True)
    )
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", repoint)])
    ]


# --- clause: a result resting on a test case not accepted is warned ----------


def as_unaccepted(findings):
    return [(f.requirement, list(f.unaccepted)) for f in findings if f.unaccepted]


def test_a_drafted_test_case_of_a_landed_requirement_is_warned(tmp_path, ctf, capsys):
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").sr("SR-002", "Accepted")
    h.tc("TC-001", ["SR-001"], "Accepted").tc("TC-002", ["SR-001"], "Drafted")
    h.tc("TC-003", ["SR-002"], "Drafted").act("two accepted, two drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    findings = _judge(ctf, h.root)
    # SR-002 has no code, so its drafted test case is not judged yet.
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unaccepted(findings) == [("SR-001", ["TC-002"])]
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    line = [ln for ln in out.splitlines() if "SR-001" in ln]
    assert len(line) == 1, out
    for token in ("WARN", "TC-002", "not accepted", "may not reflect"):
        assert token in line[0], (token, line[0])
    assert "TC-001" not in line[0] and "SR-002" not in out, out
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


def test_a_re_pointing_awaiting_its_act_is_not_accepted_for_the_requirement(
    tmp_path, ctf
):
    # TC-001 reads Accepted at the tip and names SR-001 there, but the record
    # holds it accepted only while it named SR-002: no act has accepted it for
    # SR-001 yet, so its run is evidence for text nobody accepted.
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").sr("SR-002", "Accepted")
    h.tc("TC-001", ["SR-002"], "Accepted").act("TC-001 accepted for SR-002")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    h.tc("TC-001", ["SR-001"], "Accepted").commit("TC-001 re-pointed: the text")
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unaccepted(findings) == [("SR-001", ["TC-001"])]
    assert as_unread(findings) == []


def test_a_late_acceptance_carries_the_same_warning(tmp_path, capsys, ctf):
    h = _one_finding_history(tmp_path / "repo")
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    line = [ln for ln in out.splitlines() if "SR-001" in ln]
    assert len(line) == 1 and "may not reflect" in line[0], out


# --- clause: unreadable history is reported, never a pass --------------------


def _one_finding_history(root):
    h = History(root)
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted").act("draft")
    h.write("src/app.py", implements("SR-001")).commit("implementation")
    h.tc("TC-001", ["SR-001"], "Accepted").act("accept")
    return h


def _assert_unreadable(ctf, root, start=None):
    reason = ctf.history_unreadable(root, start)
    assert reason, "expected an unreadable history"
    with pytest.raises(ctf.HistoryUnreadable):
        ctf.test_first_findings(root, src="src", start=start)
    return reason


def test_a_shallow_clone_is_reported_unreadable_never_passing(tmp_path, ctf):
    # The Trust ruling's shallow state: an act's commit may lie beyond the
    # window, so nothing is judged.
    h = _one_finding_history(tmp_path / "repo")
    shallow = tmp_path / "shallow"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", h.root.as_uri(), str(shallow)],
        check=True,
        capture_output=True,
    )
    assert "shallow" in _assert_unreadable(ctf, shallow)
    proc = run_py(
        [SCRIPTS / "check_test_first.py", "--root", ".", "--src", "src"], cwd=shallow
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "unreadable" in proc.stdout and "OK" not in proc.stdout, proc.stdout
    strict = run_py(
        [SCRIPTS / "check_test_first.py", "--root", ".", "--src", "src", "--strict"],
        cwd=shallow,
    )
    assert strict.returncode == 1, strict.stdout + strict.stderr


def test_a_start_commit_that_does_not_exist_is_reported_unreadable(tmp_path, ctf):
    h = _one_finding_history(tmp_path / "repo")
    missing = "0123456789abcdef0123456789abcdef01234567"
    assert missing[:10] in _assert_unreadable(ctf, h.root, missing)


def test_a_start_off_the_first_parent_history_is_reported_unreadable(tmp_path, ctf):
    # `side` IS an ancestor of the tip, but only through the merge's second
    # parent: it never stood on trunk, so no acceptance before it is "before the
    # start" in trunk's order.
    h = _one_finding_history(tmp_path / "repo")
    _git(h.root, "checkout", "-q", "-b", "side")
    side = h.write("src/side.py", "x = 1\n").commit("side work", registries=False)
    _git(h.root, "checkout", "-q", "main")
    _git(h.root, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    assert _git(h.root, "merge-base", "--is-ancestor", side, "HEAD") == ""
    assert "first-parent" in _assert_unreadable(ctf, h.root, side)


SR_CSV = "docs/requirements/system-requirements.csv"
TC_CSV = "docs/test/test-cases.csv"


def _csv_then_toml(root):
    """A history whose registries start under the CSV carrier and whose record
    is seeded there: SR-001 accepted, then implemented; the registries move
    to TOML; SR-002, drafted at the cutover, is implemented, then accepted,
    then its test case accepted late."""
    h = History(root)
    # The same text the TOML rows carry, so the cutover moves no accepted text.
    h.write(
        SR_CSV,
        "SR-ID,Title,Status\nSR-001,requirement SR-001,Accepted\n"
        "SR-002,requirement SR-002,Drafted\n",
    )
    h.write(TC_CSV, "TC-ID,Verifies,Status\nTC-001,SR-001,Accepted\n")
    _snapshot().copy_live(h.root, seed=True)
    csv = h.commit("the csv carrier, and the record seeded", registries=False)
    old = h.write("src/old.py", implements("SR-001")).commit("old code", False)
    for rel in (SR_CSV, TC_CSV):
        (h.root / rel).unlink()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Accepted")
    h.sr("SR-002", "Drafted").tc("TC-002", ["SR-002"], "Drafted")
    cutover = h.commit("the toml cutover")
    landing = h.write("src/new.py", implements("SR-002")).commit("new code")
    h.sr("SR-002", "Accepted").act("SR-002 accepted")
    late = h.tc("TC-002", ["SR-002"], "Accepted").act("TC-002 accepted late")
    return h, csv, old, cutover, landing, late


def test_a_start_before_the_toml_registries_is_reported_unreadable(tmp_path, ctf):
    h, csv, _old, cutover, _landing, _late = _csv_then_toml(tmp_path / "repo")
    assert "TOML" in _assert_unreadable(ctf, h.root, csv)
    # A start at or after the cutover reads, and so does no start at all:
    # pre-TOML history no longer silences the whole check.
    assert ctf.history_unreadable(h.root, cutover) is None
    assert ctf.history_unreadable(h.root) is None


def test_the_records_copies_are_read_under_either_carrier(tmp_path, ctf):
    # The record's copies follow the live carrier at each act, and either
    # carrier reads the same rows, so the registries' move to TOML dates
    # nothing: SR-001's test case keeps the record's first copy, before the
    # old code landed, and SR-002 is judged exactly in the same run.
    h, csv, old, _cutover, landing, late = _csv_then_toml(tmp_path / "repo")
    record = ctf.record_acceptances(h.root)
    assert record.pairs[("TC-001", "SR-001")] == ctf.Acceptance(csv, False)
    assert record.pairs[("TC-002", "SR-002")] == ctf.Acceptance(late, True)
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-002", landing, [("TC-002", late)])]
    assert as_unread(findings) == []


def test_registries_still_under_an_older_carrier_are_reported_unreadable(tmp_path, ctf):
    h = History(tmp_path / "repo")
    h.write(TC_CSV, "TC-ID,Verifies,Status\nTC-001,SR-001,Drafted\n")
    h.commit("the csv carrier, never moved", registries=False)
    assert "older carrier" in _assert_unreadable(ctf, h.root)


LLR_CSV = "docs/requirements/low-level-requirements.csv"


def test_a_design_registry_still_under_an_older_carrier_is_reported_unreadable(
    tmp_path, ctf
):
    # A test case reaches a requirement through a design row, so a design
    # registry the TOML reader cannot see would silently drop that test case.
    h = History(tmp_path / "repo")
    h.write(LLR_CSV, "LLR-ID,SR-Refs,Status\nLLR-001,SR-001,Accepted\n")
    h.sr("SR-001", "Accepted").tc("TC-001", ["LLR-001"], "Drafted").commit("mixed")
    h.write("src/app.py", implements("SR-001")).commit("implementation")
    assert "older carrier" in _assert_unreadable(ctf, h.root)


def _design_csv_then_toml(root):
    """TC-001 and TC-002 accepted through design rows in the record's seed
    while the design registry is CSV; SR-001's code lands; the design registry
    moves to TOML; then LLR-002 is re-pointed from SR-002 to SR-001 and
    re-accepted."""
    h = History(root)
    h.write(
        LLR_CSV,
        "LLR-ID,SR-Refs,Status\nLLR-001,SR-001,Accepted\nLLR-002,SR-002,Accepted\n",
    )
    h.sr("SR-001", "Accepted").sr("SR-002", "Accepted")
    h.tc("TC-001", ["LLR-001"], "Accepted").tc("TC-002", ["LLR-002"], "Accepted")
    csv = h.act("design rows under the csv carrier, and the record seeded")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    (h.root / LLR_CSV).unlink()
    cutover = h.llr("LLR-001", "SR-001").llr("LLR-002", "SR-002").commit("to toml")
    h.llr("LLR-002", "SR-001")
    repoint = h.act("LLR-002 re-pointed at SR-001", reaccepts=["LLR-002"])
    return h, csv, landing, cutover, repoint


def test_a_start_before_the_design_registry_moved_to_toml_is_unreadable(tmp_path, ctf):
    h, csv, _landing, cutover, _repoint = _design_csv_then_toml(tmp_path / "repo")
    assert "TOML" in _assert_unreadable(ctf, h.root, csv)
    assert ctf.history_unreadable(h.root, cutover) is None


def test_an_association_across_the_design_registrys_move_to_toml(tmp_path, ctf):
    # TC-001 reached SR-001 through LLR-001 in the record's first copy, under
    # the CSV carrier, so it is dated at or before that copy and the move to
    # TOML leaves it there; LLR-002's re-pointing after the move is an act,
    # dated exactly.
    h, csv, landing, _cutover, repoint = _design_csv_then_toml(tmp_path / "repo")
    pairs = ctf.record_acceptances(h.root).pairs
    assert pairs[("TC-001", "SR-001")] == ctf.Acceptance(csv, False)
    assert pairs[("TC-002", "SR-002")] == ctf.Acceptance(csv, False)
    assert pairs[("TC-002", "SR-001")] == ctf.Acceptance(repoint, True)
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [("TC-002", repoint)])]
    assert as_unread(findings) == []


def test_an_acceptance_under_a_retired_status_word_has_no_exact_date(tmp_path, ctf):
    # A move into `Accepted` from a word outside the closed vocabulary is a
    # rename, not the act: the row was accepted at or before it. Renamed before
    # the landing, it is not late; renamed after, its order cannot be read. The
    # first act seeds the record, so its copy holds the retired word.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Verified")
    h.tc("TC-002", ["SR-001"], "Verified").act("the old vocabulary")
    early = h.tc("TC-002", ["SR-001"], "Accepted").act("TC-002 renamed")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    renamed = h.tc("TC-001", ["SR-001"], "Accepted").act("TC-001 renamed")
    assert ctf.record_acceptances(h.root).tests == {
        "TC-002": ctf.Acceptance(early, False),
        "TC-001": ctf.Acceptance(renamed, False),
    }
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", renamed)])]
    # An unread order is never a pass: with no late acceptance anywhere, the
    # unread requirement alone fails the run once --strict promotes it.
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


def test_a_requirement_renamed_into_acceptance_after_the_start_cannot_be_judged(
    tmp_path, ctf
):
    # Its own acceptance is at or before the rename, which follows the start, so
    # whether it was accepted after the start cannot be read.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Verified").tc("TC-001", ["SR-001"], "Drafted").act("old")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    start = h.write("notes.txt", "adopted\n").commit("the rule adopted", False)
    renamed = h.sr("SR-001", "Accepted").act("SR-001 renamed")
    h.tc("TC-001", ["SR-001"], "Accepted").act("TC-001 accepted late")
    findings = _judge(ctf, h.root, start=start)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("SR-001", renamed)])]


# --- TC-468: an act's commit dates the rows it names --------------------------


def test_a_re_pointing_committed_before_its_act_is_dated_at_the_act(tmp_path, ctf):
    """Text then act, as the commit hook requires on trunk: TC-001's re-pointing
    is committed as text BEFORE SR-001's code lands, and the act re-accepting
    it comes after. The pair is accepted at the act the ledger records, so it
    is late; a replay of the live registry dates it at the text commit, before
    the landing, and reports nothing.

    Implements: TC-468"""
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").sr("SR-002", "Accepted")
    h.tc("TC-001", ["SR-002"], "Accepted").act("TC-001 accepted for SR-002")
    h.tc("TC-001", ["SR-001"], "Accepted").commit("TC-001 re-pointed: the text")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    act = h.act("TC-001 re-accepted for SR-001", reaccepts=["TC-001"])
    assert as_tuples(_judge(ctf, h.root)) == [("SR-001", landing, [("TC-001", act)])]


def test_an_act_on_a_side_branch_is_ordered_where_it_reached_trunk(tmp_path, ctf):
    """TC-001 is accepted by an act on a side branch before SR-001's code lands
    on trunk, but the branch is merged after the landing: on trunk the
    acceptance arrives at the merge, after the code, as a landing would. The
    report names the act's own commit.

    Implements: TC-468"""
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted").act("drafted")
    _git(h.root, "checkout", "-q", "-b", "side")
    side = h.tc("TC-001", ["SR-001"], "Accepted").act("TC-001 accepted on a branch")
    _git(h.root, "checkout", "-q", "main")
    landing = h.write("src/app.py", implements("SR-001")).commit("code", False)
    _git(h.root, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    merge = _git(h.root, "rev-parse", "HEAD")
    record = ctf.record_acceptances(h.root)
    trunk = _git(h.root, "rev-list", "--first-parent", "--reverse", "HEAD").split()
    assert side not in trunk
    assert record.places[side] == trunk.index(merge)
    assert as_tuples(_judge(ctf, h.root)) == [("SR-001", landing, [("TC-001", side)])]


# --- TC-469: the record's cut --------------------------------------------------


def _earlier_record(h, entries):
    """The record as an earlier spelling held it: copies equal to live under
    its earlier directory, and a ledger whose entries use the earlier keys."""
    for rel in TABLES:
        if (h.root / rel).is_file():
            dest = h.root / EARLIER / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(h.root / rel, dest)
    lines = []
    for seq, approved in enumerate(entries, 1):
        lines += [
            "[[act]]",
            "seq = {}".format(seq),
            'date = "2026-09-27"',
            "approved = {}".format(_cell(approved) if approved else "[]"),
            "reattested = []",
            "",
        ]
    h.write(EARLIER + "/acts.toml", "\n".join(lines))


def _the_cut(root):
    """An earlier-spelling record (directory, ledger keys, status `Approved`)
    with two acts on trunk, SR-001's code landing between them; then, on a
    side branch, the move into the current spelling, merged onto trunk; then
    a later act, and SR-002's code."""
    h = History(root)
    h.sr("SR-001", "Approved").sr("SR-002", "Approved")
    h.tc("TC-001", ["SR-001"], "Drafted").tc("TC-002", ["SR-002"], "Approved")
    h._registries()
    _earlier_record(h, [["SR-001", "SR-002", "TC-002"]])
    h.commit("the record, in an earlier spelling", registries=False)
    landing = h.write("src/a.py", implements("SR-001")).commit("SR-001 code")
    h.tc("TC-001", ["SR-001"], "Approved")._registries()
    _earlier_record(h, [["SR-001", "SR-002", "TC-002"], ["TC-001"]])
    old_act = h.commit("TC-001 accepted after the landing, in the earlier spelling")
    _git(h.root, "checkout", "-q", "-b", "vocabulary")
    shutil.rmtree(h.root / EARLIER)
    for rid in ("SR-001", "SR-002"):
        h.sr(rid, "Accepted")
    h.tc("TC-001", ["SR-001"], "Accepted").tc("TC-002", ["SR-002"], "Accepted")
    h._registries()
    for rel in TABLES:
        if (h.root / rel).is_file():
            dest = h.root / RECORD / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(h.root / rel, dest)
    h.write(
        LEDGER,
        '[[act]]\nseq = 1\ndate = "2026-09-27"\n'
        'accepted = ["SR-001", "SR-002", "TC-002"]\nreaccepted = []\n\n'
        '[[act]]\nseq = 2\ndate = "2026-09-27"\naccepted = ["TC-001"]\n'
        "reaccepted = []\n",
    )
    move = h.commit("the record moves into the current spelling", registries=False)
    _git(h.root, "checkout", "-q", "main")
    _git(h.root, "merge", "-q", "--no-ff", "vocabulary", "-m", "merge the cut")
    trunk = _git(h.root, "rev-parse", "HEAD")
    later = h.tc("TC-003", ["SR-002"], "Accepted").act("TC-003 accepted for SR-002")
    second = h.write("src/b.py", implements("SR-002")).commit("SR-002 code", False)
    return h, landing, old_act, move, trunk, second, later


def test_the_record_before_its_cut_is_never_read(tmp_path, ctf):
    """The move is the record's cut: what it carries is known only to be at or
    before the commit that brought it onto trunk. SR-001's code landed before
    that, so TC-001's order against it cannot be read; it is never dated at
    the act the earlier spelling records (which would make it late), nor at
    a later act. SR-002's code landed after the cut reached trunk, so the
    cut's date settles TC-002, and TC-003's act before that code is exact.

    Implements: TC-469"""
    h, landing, old_act, move, trunk, _second, later = _the_cut(tmp_path / "repo")
    record = ctf.record_acceptances(h.root)
    assert record.cuts == [move] and record.gaps == []
    assert record.pairs[("TC-001", "SR-001")] == ctf.Acceptance(move, False)
    assert record.pairs[("TC-002", "SR-002")] == ctf.Acceptance(move, False)
    assert record.pairs[("TC-003", "SR-002")] == ctf.Acceptance(later, True)
    line = _git(h.root, "rev-list", "--first-parent", "--reverse", "HEAD").split()
    assert record.places[move] == line.index(trunk)
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", move)])]
    assert old_act not in str(findings)
    # Declared at the commit that brought the cut onto trunk, as this
    # repository declares it, every requirement the cut carries is out of
    # scope.
    assert _judge(ctf, h.root, start=trunk) == []


# --- TC-470: no record, or an empty ledger ------------------------------------


def _accepted_without_an_act(root, empty_ledger):
    h = History(root)
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Accepted")
    if empty_ledger:
        h.write(LEDGER, "# ACCEPTANCE ACTS, appended by `intake.py snapshot`.\n")
    start = h.commit("rows accepted with no act on record")
    landing = h.write("src/app.py", implements("SR-001")).commit("code")
    return h, start, landing


@pytest.mark.parametrize("empty_ledger", [False, True])
def test_acceptances_no_act_records_are_unread_never_passing(
    tmp_path, ctf, empty_ledger
):
    """Rows reading accepted with no act on record, under no record at all
    and under a record holding only an empty ledger: no act dates them, so
    the order is unread, never a pass, and --strict refuses it.

    Implements: TC-470"""
    h, start, landing = _accepted_without_an_act(tmp_path / "repo", empty_ledger)
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", None)])]
    # With a start, whether the requirement entered scope cannot be read either.
    scoped = _judge(ctf, h.root, start=start)
    assert as_unread(scoped) == [("SR-001", [("SR-001", None)])]
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


def _cut_without_an_act(root, ledger):
    """The record's first copy holds SR-001 and TC-001 accepted beside a
    ledger that is `absent`, `empty` or `malformed`, and SR-001's code lands
    after it, so a date at or before the cut would settle the order."""
    h = History(root)
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Accepted")._registries()
    for rel in TABLES:
        if (h.root / rel).is_file():
            dest = h.root / RECORD / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(h.root / rel, dest)
    if ledger == "empty":
        h.write(LEDGER, "# ACCEPTANCE ACTS, appended by `intake.py snapshot`.\n")
    elif ledger == "malformed":
        entry = (
            '[[act]]\nseq = 1\ndate = "2026-11-22"\naccepted = ["SR-001", "TC-001"]\n'
            'reaccepted = []\ncopied = ["{}", "{}"]\n'.format(SR_REG, TC_REG)
        )
        h.write(LEDGER, entry + "\n" + entry)  # two entries numbered 1
    cut = h.commit("the record's first copy", registries=False)
    landing = h.write("src/app.py", implements("SR-001")).commit("code")
    return h, cut, landing


@pytest.mark.parametrize("ledger", ["absent", "empty"])
def test_a_cut_whose_ledger_holds_no_act_is_unread(tmp_path, ctf, ledger):
    """The record's first copy holds accepted rows, but its ledger holds no
    act: no act vouches for the copy, so what it carries is unread, never
    settled by the cut's date, although the code landed after the cut.

    Implements: TC-470"""
    h, cut, landing = _cut_without_an_act(tmp_path / "repo", ledger)
    assert ctf.record_acceptances(h.root).cuts == [cut]
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", cut)])]
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


# --- TC-471: a change to the record with no act, and a malformed ledger -------


def test_a_cut_whose_ledger_is_malformed_is_unread(tmp_path, ctf):
    """The record's first copy holds accepted rows beside a ledger that
    numbers two entries alike: which acts it records cannot be read, so what
    the cut carries is unread, never settled by the cut's date.

    Implements: TC-471"""
    h, cut, landing = _cut_without_an_act(tmp_path / "repo", "malformed")
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", cut)])]
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


def test_a_record_change_with_no_act_is_unread_never_dated_later(tmp_path, ctf):
    """The test-case copy is rewritten, flipping TC-001, in a commit that adds
    no ledger entry: a gap. A later act copies the registry again; TC-001's
    acceptance stays unread at the gap, never dated at that act.

    Implements: TC-471"""
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Drafted").act("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("code")
    h.tc("TC-001", ["SR-001"], "Accepted")._registries()
    (h.root / RECORD / TC_REG).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(h.root / TC_REG, h.root / RECORD / TC_REG)
    gap = h.commit("TC-001 flipped in the record with no act", registries=False)
    later = h.tc("TC-002", ["SR-001"], "Accepted").act("TC-002 accepted")
    record = ctf.record_acceptances(h.root)
    assert record.gaps == [gap]
    assert record.pairs[("TC-001", "SR-001")].unread
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [("TC-002", later)])]
    assert as_unread(findings) == [("SR-001", [("TC-001", gap)])]


def test_an_act_whose_ledger_is_malformed_is_unread(tmp_path, ctf):
    """The act's committed ledger numbers its entry like the one before it, so
    which acts that commit added cannot be read: what it carries is unread.

    Implements: TC-471"""
    h = History(tmp_path / "repo")
    h.seed()
    h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted").act("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("code")
    h.tc("TC-001", ["SR-001"], "Accepted")._registries()
    _snapshot().copy_live(h.root)
    ledger = h.root / LEDGER
    text = ledger.read_text(encoding="utf-8")
    ledger.write_text(text.replace("seq = 3", "seq = 2"), encoding="utf-8")
    bad = h.commit("TC-001 accepted, its ledger entry misnumbered", False)
    record = ctf.record_acceptances(h.root)
    assert record.gaps == [bad]
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", bad)])]


# --- clause: order is read only from commits, never from a cell --------------


def test_the_order_comes_from_commits_never_from_a_cell(tmp_path, ctf):
    # Two histories ending in byte-identical trees: every cell of every row is
    # the same at the tip, so any difference in the verdict came from history.
    def build(root, test_first):
        h = History(root)
        h.seed()
        h.sr("SR-001", "Accepted").tc("TC-001", ["SR-001"], "Drafted").act("draft")
        steps = [
            lambda: h.tc("TC-001", ["SR-001"], "Accepted").act("accept"),
            lambda: h.write("src/app.py", implements("SR-001")).commit("implement"),
        ]
        for step in steps if test_first else reversed(steps):
            step()
        return h

    first = build(tmp_path / "test-first", True)
    after = build(tmp_path / "test-after", False)
    tree = "HEAD^{tree}"
    assert _git(first.root, "rev-parse", tree) == _git(after.root, "rev-parse", tree)
    assert _judge(ctf, first.root) == []
    assert [f.requirement for f in _judge(ctf, after.root)] == ["SR-001"]


# --- clause: the step lists as warn-only in the harness plan -----------------


def test_the_step_lists_as_warn_only_in_the_harness_plan(tmp_path):
    check = load_script("check")
    ladder = check._kitladder
    assert "test-first" in check.BUILTIN_STEP_NAMES
    plan = {s[0]: s for s in check.steps(80, "full", "all")}
    _name, _requires, cmd, threshold, layer = plan["test-first"]
    assert threshold == ladder.STAGE_ORDER[0] and layer == "process"
    assert cmd[1].endswith("check_test_first.py") and "--strict" not in cmd
    # The listing at the lowest rung carries it, with no promotion flag.
    h = _one_finding_history(tmp_path / "repo")
    listed = run_py(
        [SCRIPTS / "check.py", "--stage", ladder.STAGE_ORDER[0], "--list"], cwd=h.root
    )
    assert listed.returncode == 0, listed.stdout + listed.stderr
    line = [ln for ln in listed.stdout.splitlines() if " test-first " in ln]
    assert len(line) == 1 and "check_test_first.py" in line[0], listed.stdout
    assert "--strict" not in line[0], line[0]
    # Warn-only in effect: the harness step passes over a history with a
    # finding and prints it, while the same command promoted by --strict
    # refuses — so the missing flag is the whole of the decision.
    ran = run_py([SCRIPTS / "check.py", "--run-step", "test-first"], cwd=h.root)
    assert ran.returncode == 0, ran.stdout + ran.stderr
    assert "PASS" in ran.stdout and "SR-001" in ran.stdout, ran.stdout
    strict = run_py([*cmd[1:], "--strict"], cwd=h.root)
    assert strict.returncode == 1, strict.stdout + strict.stderr


# --- the declared start's reader (LLR-257: a string reader beside process_check)


def test_the_start_reader_answers_text_none_or_refuses(tmp_path):
    load_script("check")  # puts scripts/ on sys.path, so the package imports
    from kitlib import config

    docs = tmp_path / "docs"
    docs.mkdir()
    assert config.process_check_text(tmp_path, "test_first_since") is None
    toml = docs / "process.toml"
    for text, expected in (
        ("[checks]\n", None),
        ('[checks]\ntest_first_since = ""\n', None),
        ('[checks]\ntest_first_since = "  abc123  "\n', "abc123"),
    ):
        toml.write_text(text, encoding="utf-8")
        assert config.process_check_text(tmp_path, "test_first_since") == expected
    for bad in ("[checks]\ntest_first_since = true\n", "[checks\n"):
        toml.write_text(bad, encoding="utf-8")
        with pytest.raises(ValueError):
            config.process_check_text(tmp_path, "test_first_since")
