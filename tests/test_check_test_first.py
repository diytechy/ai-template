"""Verifies SR-217 / LLR-257 (TC-250) — the test-first order, read from history.

Every case drives `check_test_first.py` over a REAL git repository built commit
by commit, which is why the module is registered in conftest.SLOW_MODULES: the
order under test exists only in commits, so no in-memory fixture can stand in
for it. Most cases call the module's functions in-process on those repositories;
the cases about what the harness reads back (the printed report, the exit code,
the plan listing) run the delivered commands as subprocesses.

Each `History` commit rewrites the three registries whole from the rows declared
so far, so a commit's diff is exactly the rows the case changed in it.
"""

import subprocess

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, skip_without_env_gates

SR_REG = "docs/requirements/system-requirements.toml"
LLR_REG = "docs/requirements/low-level-requirements.toml"
TC_REG = "docs/test/test-cases.toml"
TABLES = {SR_REG: "requirement", LLR_REG: "design", TC_REG: "test"}


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

    def llr(self, rid, sr, status="Approved"):
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


def implements(*ids):
    """A source file whose one declaration line names `ids`."""
    return '"""A module.\n\nImplements: {}\n"""\n'.format(", ".join(ids))


def as_tuples(findings):
    return [(f.requirement, f.implementation, list(f.late)) for f in findings]


def as_unread(findings):
    return [(f.requirement, list(f.unread)) for f in findings if f.unread]


def _judge(ctf, root, start=None):
    return ctf.test_first_findings(root, src="src", start=start)


# --- clause: test cases approved first produce nothing ------------------------


def test_test_cases_all_approved_before_the_implementation_produce_nothing(
    tmp_path, ctf
):
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Approved")
    h.commit("requirement, one test case approved")
    h.tc("TC-001", ["SR-001"], "Approved")
    h.commit("second test case approved")
    h.write("src/app.py", implements("SR-001"))
    h.commit("implementation")
    assert _judge(ctf, h.root) == []


# --- clause: landing through the requirement or a design row, earlier wins ----


@pytest.mark.parametrize("first", ["SR-001", "LLR-001"])
def test_the_landing_is_the_earlier_of_a_requirement_line_and_a_design_row_line(
    tmp_path, ctf, first
):
    # The test case is approved BETWEEN the two declaring commits, so the report
    # exists only if the landing is read at the earlier one, whichever id it
    # names; a landing read at the later line would put the approval first.
    later = "LLR-001" if first == "SR-001" else "SR-001"
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").llr("LLR-001", "SR-001")
    h.tc("TC-001", ["SR-001", "LLR-001"], "Drafted")
    h.commit("chain drafted")
    landing = h.write("src/a.py", implements(first)).commit("first declaration")
    approval = h.tc("TC-001", ["SR-001", "LLR-001"], "Approved").commit("approve")
    h.write("src/b.py", implements(later)).commit("second declaration")
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", approval)])
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


# --- clause: two late test cases, both approval commits named -----------------


def test_two_test_cases_approved_after_the_landing_are_both_named(tmp_path, ctf):
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Drafted")
    h.commit("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    one = h.tc("TC-001", ["SR-001"], "Approved").commit("approve TC-001")
    two = h.tc("TC-002", ["SR-001"], "Approved").commit("approve TC-002")
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", one), ("TC-002", two)])
    ]


def test_the_printed_report_names_the_requirement_and_every_commit(tmp_path):
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Drafted")
    h.commit("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    one = h.tc("TC-001", ["SR-001"], "Approved").commit("approve TC-001")
    two = h.tc("TC-002", ["SR-001"], "Approved").commit("approve TC-002")
    proc = run_py(
        [SCRIPTS / "check_test_first.py", "--root", ".", "--src", "src"], cwd=h.root
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    lines = [ln for ln in proc.stdout.splitlines() if "SR-001" in ln]
    assert len(lines) == 1, proc.stdout
    for token in ("WARN", "TC-001", "TC-002", landing[:10], one[:10], two[:10]):
        assert token in lines[0], (token, lines[0])


# --- clause: approving one while withdrawing another --------------------------


def test_a_commit_approving_one_test_case_while_withdrawing_another_records_it(
    tmp_path, ctf
):
    # The approved-status count is the same on both sides of the swap, which is
    # why an occurrence-count pickaxe over the registry would see no change here.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted")
    h.tc("TC-002", ["SR-001"], "Approved")
    h.commit("drafted and approved")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    h.tc("TC-001", ["SR-001"], "Approved").tc("TC-002", ["SR-001"], "Drafted")
    swap = h.commit("approve TC-001, withdraw TC-002")
    root_commit = _git(h.root, "rev-list", "--max-parents=0", "HEAD")
    assert ctf.first_approval_commits(h.root, TC_REG, "TC-ID") == {
        "TC-002": ctf.Approval(root_commit, True),
        "TC-001": ctf.Approval(swap, True),
    }
    assert as_tuples(_judge(ctf, h.root)) == [("SR-001", landing, [("TC-001", swap)])]


def test_a_withdrawn_and_reapproved_test_case_keeps_its_first_approval(tmp_path, ctf):
    # LLR-257 records each row's FIRST move into approval. Re-approving after a
    # withdrawal is not that move, from the root or from a declared start.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Approved")
    first = h.commit("test case approved first")
    start = h.write("src/app.py", implements("SR-001")).commit("implementation")
    h.tc("TC-001", ["SR-001"], "Drafted").commit("withdrawn")
    h.tc("TC-001", ["SR-001"], "Approved").commit("re-approved")
    approvals = ctf.first_approval_commits(h.root, TC_REG, "TC-ID")
    assert approvals == {"TC-001": ctf.Approval(first, True)}
    # Walked from a later commit, the row was already approved there: approved
    # at or before it, on a date that walk cannot narrow.
    later = ctf.first_approval_commits(h.root, TC_REG, "TC-ID", since=start)
    assert later == {"TC-001": ctf.Approval(start, False)}
    assert _judge(ctf, h.root) == []
    assert _judge(ctf, h.root, start=start) == []


# --- clause: no implementation produces nothing ------------------------------


def test_a_requirement_with_no_implementation_produces_nothing(tmp_path, ctf):
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted")
    h.write("src/app.py", "# relates to SR-001, but declares nothing\n")
    h.commit("drafted")
    h.tc("TC-001", ["SR-001"], "Approved").commit("approve")
    assert _judge(ctf, h.root) == []


# --- clause: a declared start scopes the requirements judged ----------------


def _two_requirements(root):
    """SR-001 approved in the root commit, SR-002 approved after `start`; both
    implemented at `start`, both with a test case approved after it."""
    h = History(root)
    h.sr("SR-001", "Approved").sr("SR-002", "Drafted")
    h.tc("TC-001", ["SR-001"], "Drafted").tc("TC-002", ["SR-002"], "Drafted")
    h.commit("SR-001 approved")
    start = h.write("src/app.py", implements("SR-001", "SR-002")).commit("impl")
    h.sr("SR-002", "Approved").commit("SR-002 approved")
    h.tc("TC-001", ["SR-001"], "Approved").tc("TC-002", ["SR-002"], "Approved")
    late = h.commit("both test cases approved")
    return h, start, late


def test_a_declared_start_after_a_requirements_approval_excludes_it(tmp_path, ctf):
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


def test_a_test_case_approved_after_the_landing_but_before_the_start_is_reported(
    tmp_path, ctf
):
    # SR-217 scopes only the REQUIREMENT's approval to the start. A test case's
    # approval is its earliest approving commit over the whole history, so a
    # test case approved after the code landed stays late even when both
    # happened before the start the requirement was approved after.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Drafted").tc("TC-001", ["SR-001"], "Drafted").commit("drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    approval = h.tc("TC-001", ["SR-001"], "Approved").commit("test case approved")
    start = h.write("notes.txt", "adopted\n").commit("the rule adopted", False)
    h.sr("SR-001", "Approved").commit("requirement approved after the start")
    assert as_tuples(_judge(ctf, h.root, start=start)) == [
        ("SR-001", landing, [("TC-001", approval)])
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


# --- clause: a test case born approved counts at its birth -------------------


def test_a_test_case_added_already_approved_counts_at_its_birth(tmp_path, ctf):
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").commit("requirement")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    born = h.tc("TC-001", ["SR-001"], "Approved").commit("test case, born approved")
    assert ctf.first_approval_commits(h.root, TC_REG, "TC-ID") == {
        "TC-001": ctf.Approval(born, True)
    }
    assert as_tuples(_judge(ctf, h.root)) == [("SR-001", landing, [("TC-001", born)])]


# --- clause: a test case is the requirement's from its approved-and-naming commit


def test_an_approved_test_case_re_pointed_after_the_landing_is_dated_at_the_re_point(
    tmp_path, ctf
):
    # TC-001 was approved long before SR-001's code, but for SR-002. Named at
    # SR-001 only after the code landed, it is SR-001's test case from that
    # commit: its own earlier approval date does not travel with it.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").sr("SR-002", "Approved")
    h.tc("TC-001", ["SR-002"], "Approved")
    early = h.commit("TC-001 approved for SR-002")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    repoint = h.tc("TC-001", ["SR-001"], "Approved").commit("TC-001 re-pointed")
    assert ctf.first_association_commits(h.root) == {
        ("TC-001", "SR-002"): ctf.Approval(early, True),
        ("TC-001", "SR-001"): ctf.Approval(repoint, True),
    }
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", repoint)])
    ]


def test_a_test_case_reaching_the_requirement_through_a_re_pointed_design_row(
    tmp_path, ctf
):
    # TC-001 names LLR-001 throughout and is approved first. LLR-001 belonged to
    # SR-002 and is re-pointed at SR-001 after SR-001's code landed, so TC-001
    # names one of SR-001's design rows only from the re-pointing commit.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").sr("SR-002", "Approved").llr("LLR-001", "SR-002")
    h.tc("TC-001", ["LLR-001"], "Approved").commit("TC-001 approved via LLR-001")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    repoint = h.llr("LLR-001", "SR-001").commit("LLR-001 re-pointed at SR-001")
    assert ctf.first_association_commits(h.root)[("TC-001", "SR-001")] == (
        ctf.Approval(repoint, True)
    )
    assert as_tuples(_judge(ctf, h.root)) == [
        ("SR-001", landing, [("TC-001", repoint)])
    ]


# --- clause: a result resting on a test case not approved is warned ----------


def as_unapproved(findings):
    return [(f.requirement, list(f.unapproved)) for f in findings if f.unapproved]


def test_a_drafted_test_case_of_a_landed_requirement_is_warned(tmp_path, ctf, capsys):
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").sr("SR-002", "Approved")
    h.tc("TC-001", ["SR-001"], "Approved").tc("TC-002", ["SR-001"], "Drafted")
    h.tc("TC-003", ["SR-002"], "Drafted").commit("two approved, two drafted")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    findings = _judge(ctf, h.root)
    # SR-002 has no code, so its drafted test case is not judged yet.
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unapproved(findings) == [("SR-001", ["TC-002"])]
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    line = [ln for ln in out.splitlines() if "SR-001" in ln]
    assert len(line) == 1, out
    for token in ("WARN", "TC-002", "not approved", "may not reflect"):
        assert token in line[0], (token, line[0])
    assert "TC-001" not in line[0] and "SR-002" not in out, out
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


def test_a_late_approval_carries_the_same_warning(tmp_path, capsys, ctf):
    h = _one_finding_history(tmp_path / "repo")
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    line = [ln for ln in out.splitlines() if "SR-001" in ln]
    assert len(line) == 1 and "may not reflect" in line[0], out


# --- clause: unreadable history is reported, never a pass --------------------


def _one_finding_history(root):
    h = History(root)
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted").commit("draft")
    h.write("src/app.py", implements("SR-001")).commit("implementation")
    h.tc("TC-001", ["SR-001"], "Approved").commit("approve")
    return h


def _assert_unreadable(ctf, root, start=None):
    reason = ctf.history_unreadable(root, start)
    assert reason, "expected an unreadable history"
    with pytest.raises(ctf.HistoryUnreadable):
        ctf.test_first_findings(root, src="src", start=start)
    return reason


def test_a_shallow_clone_is_reported_unreadable_never_passing(tmp_path, ctf):
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
    # parent: it never stood on trunk, so no approval before it is "before the
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
    """A history whose registries start under the CSV carrier: SR-001 approved,
    implemented and its test case approved before the TOML cutover; SR-002
    drafted at the cutover, implemented, then its test case approved late."""
    h = History(root)
    h.write(SR_CSV, "SR-ID,Status\nSR-001,Approved\n")
    h.write(TC_CSV, "TC-ID,Verifies,Status\nTC-001,SR-001,Approved\n")
    csv = h.commit("the csv carrier", registries=False)
    old = h.write("src/old.py", implements("SR-001")).commit("old code", False)
    for rel in (SR_CSV, TC_CSV):
        (h.root / rel).unlink()
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Approved")
    h.sr("SR-002", "Drafted").tc("TC-002", ["SR-002"], "Drafted")
    cutover = h.commit("the toml cutover")
    landing = h.write("src/new.py", implements("SR-002")).commit("new code")
    h.sr("SR-002", "Approved").commit("SR-002 approved")
    late = h.tc("TC-002", ["SR-002"], "Approved").commit("TC-002 approved late")
    return h, csv, old, cutover, landing, late


def test_a_start_before_the_toml_registries_is_reported_unreadable(tmp_path, ctf):
    h, csv, _old, cutover, _landing, _late = _csv_then_toml(tmp_path / "repo")
    assert "TOML" in _assert_unreadable(ctf, h.root, csv)
    # A start at or after the cutover reads, and so does no start at all:
    # pre-TOML history no longer silences the whole check.
    assert ctf.history_unreadable(h.root, cutover) is None
    assert ctf.history_unreadable(h.root) is None


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
    h.write(LLR_CSV, "LLR-ID,SR-Refs,Status\nLLR-001,SR-001,Approved\n")
    h.sr("SR-001", "Approved").tc("TC-001", ["LLR-001"], "Drafted").commit("mixed")
    h.write("src/app.py", implements("SR-001")).commit("implementation")
    assert "older carrier" in _assert_unreadable(ctf, h.root)


def _design_csv_then_toml(root):
    """TC-001 and TC-002 approved through design rows while the design
    registry is CSV; SR-001's code lands; the design registry moves to TOML;
    then LLR-002 is re-pointed from SR-002 to SR-001."""
    h = History(root)
    h.write(
        LLR_CSV,
        "LLR-ID,SR-Refs,Status\nLLR-001,SR-001,Approved\nLLR-002,SR-002,Approved\n",
    )
    h.sr("SR-001", "Approved").sr("SR-002", "Approved")
    h.tc("TC-001", ["LLR-001"], "Approved").tc("TC-002", ["LLR-002"], "Approved")
    csv = h.commit("design rows under the csv carrier")
    landing = h.write("src/app.py", implements("SR-001")).commit("SR-001 code")
    (h.root / LLR_CSV).unlink()
    cutover = h.llr("LLR-001", "SR-001").llr("LLR-002", "SR-002").commit("to toml")
    repoint = h.llr("LLR-002", "SR-001").commit("LLR-002 re-pointed at SR-001")
    return h, csv, landing, cutover, repoint


def test_a_start_before_the_design_registry_moved_to_toml_is_unreadable(tmp_path, ctf):
    h, csv, _landing, cutover, _repoint = _design_csv_then_toml(tmp_path / "repo")
    assert "TOML" in _assert_unreadable(ctf, h.root, csv)
    assert ctf.history_unreadable(h.root, cutover) is None


def test_an_association_across_the_design_registrys_move_to_toml(tmp_path, ctf):
    # TC-001 already reached SR-001 through LLR-001 under the CSV carrier, so
    # the move dates that pair only at or before itself; LLR-002's re-point
    # after the move is the act, dated exactly.
    h, _csv, landing, cutover, repoint = _design_csv_then_toml(tmp_path / "repo")
    pairs = ctf.first_association_commits(h.root)
    assert pairs[("TC-001", "SR-001")] == ctf.Approval(cutover, False)
    assert pairs[("TC-002", "SR-002")] == ctf.Approval(cutover, False)
    assert pairs[("TC-002", "SR-001")] == ctf.Approval(repoint, True)
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [("TC-002", repoint)])]
    assert as_unread(findings) == [("SR-001", [("TC-001", cutover)])]


def test_a_verdict_resting_on_a_date_before_the_toml_registries_is_unread(
    tmp_path, ctf, capsys
):
    # TC-001's approval lies before the cutover, where no date can be read, and
    # SR-001's code landed before it too: which came first cannot be known, so
    # SR-001 is reported unread, never passed. SR-002 lives wholly after the
    # cutover and is judged exactly in the same run.
    h, _csv, old, cutover, landing, late = _csv_then_toml(tmp_path / "repo")
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [
        ("SR-001", old, []),
        ("SR-002", landing, [("TC-002", late)]),
    ]
    assert as_unread(findings) == [("SR-001", [("TC-001", cutover)])]
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    out = capsys.readouterr().out
    line = [ln for ln in out.splitlines() if "SR-001" in ln]
    assert len(line) == 1 and "cannot be read" in line[0], out
    assert "OK" not in out, out


def test_an_approval_under_a_retired_status_word_has_no_exact_date(tmp_path, ctf):
    # A move into `Approved` from a word outside the closed vocabulary is a
    # rename, not the act: the row was approved at or before it. Renamed before
    # the landing, it is not late; renamed after, its order cannot be read.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Verified")
    h.tc("TC-002", ["SR-001"], "Verified").commit("the old vocabulary")
    early = h.tc("TC-002", ["SR-001"], "Approved").commit("TC-002 renamed")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    renamed = h.tc("TC-001", ["SR-001"], "Approved").commit("TC-001 renamed")
    assert ctf.first_approval_commits(h.root, TC_REG, "TC-ID") == {
        "TC-002": ctf.Approval(early, False),
        "TC-001": ctf.Approval(renamed, False),
    }
    findings = _judge(ctf, h.root)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("TC-001", renamed)])]
    # An unread order is never a pass: with no late approval anywhere, the
    # unread requirement alone fails the run once --strict promotes it.
    assert ctf.main(["--root", str(h.root), "--src", "src"]) == 0
    assert ctf.main(["--root", str(h.root), "--src", "src", "--strict"]) == 1


def test_a_requirement_renamed_into_approval_after_the_start_cannot_be_judged(
    tmp_path, ctf
):
    # Its own approval is at or before the rename, which follows the start, so
    # whether it was approved after the start cannot be read.
    h = History(tmp_path / "repo")
    h.sr("SR-001", "Verified").tc("TC-001", ["SR-001"], "Drafted").commit("old")
    landing = h.write("src/app.py", implements("SR-001")).commit("implementation")
    start = h.write("notes.txt", "adopted\n").commit("the rule adopted", False)
    renamed = h.sr("SR-001", "Approved").commit("SR-001 renamed")
    h.tc("TC-001", ["SR-001"], "Approved").commit("TC-001 approved late")
    findings = _judge(ctf, h.root, start=start)
    assert as_tuples(findings) == [("SR-001", landing, [])]
    assert as_unread(findings) == [("SR-001", [("SR-001", renamed)])]


# --- clause: order is read only from commits, never from a cell --------------


def test_the_order_comes_from_commits_never_from_a_cell(tmp_path, ctf):
    # Two histories ending in byte-identical trees: every cell of every row is
    # the same at the tip, so any difference in the verdict came from history.
    def build(root, test_first):
        h = History(root)
        h.sr("SR-001", "Approved").tc("TC-001", ["SR-001"], "Drafted").commit("draft")
        steps = [
            lambda: h.tc("TC-001", ["SR-001"], "Approved").commit("approve"),
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
