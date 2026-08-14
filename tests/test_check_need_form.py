"""check_need_form.py — SN-033's declared need-cell form check (WI-454).

SN-033's ratified acceptance commissions "a declared check [that] reports the
row and phrase when a need cell contains an internal path, implementation-only
identifier or process citation", with a reviewed exception list for names that
are themselves user-facing interfaces. The check scans `need` cells ONLY —
SN-033 exempts acceptance and engineering-requirement cells by its own text —
and is warn-first (exit 0) unless --strict. The live-registry case is the WI's
whole point: the check landed while the tier was measured clean, to lock that
state in ahead of the SR re-tier's churn.
"""

from conftest import ROOT, SCRIPTS, run_py

# A need cell carrying one token of each of the three classes SN-033 names.
DIRTY_NEED = (
    "A user can resume work from docs/status.md by setting "
    "human_ratification_through, as SR-101 and process.md §4 describe."
)


def make_repo(root, need_cell, allow=None, extra_rows=""):
    reg = root / "docs" / "requirements"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "stakeholder-needs.toml").write_text(
        "[need.SN-050]\n"
        'kind = "core"\n'
        'priority = "M"\n'
        'need = """' + need_cell + '"""\n'
        'why = """because."""\n'
        'acceptance = """when it works."""\n' + extra_rows,
        encoding="utf-8",
    )
    if allow is not None:
        (root / "docs" / "need-form-allow").write_text(allow, encoding="utf-8")
    return root


def form(root, *args):
    return run_py([SCRIPTS / "check_need_form.py", *args], cwd=root)


def test_dirty_need_cell_names_the_row_and_each_offending_phrase(tmp_path):
    make_repo(tmp_path, DIRTY_NEED)
    proc = form(tmp_path)
    assert proc.returncode == 0, "warn-first: findings must not gate by default"
    # SN-033's acceptance requires BOTH the row and the phrase in the report.
    assert "SN-050" in proc.stdout
    for phrase in ("docs/status.md", "human_ratification_through", "SR-101"):
        assert phrase in proc.stdout, "offending phrase not named: " + phrase
    # One finding per token, once: docs/status.md (path — its inner status.md
    # is NOT a second finding), human_ratification_through, process.md, §4,
    # SR-101.
    assert "5 finding(s)" in proc.stdout


def test_strict_promotes_the_same_findings_to_exit_1(tmp_path):
    make_repo(tmp_path, DIRTY_NEED)
    assert form(tmp_path, "--strict").returncode == 1


def test_a_user_facing_interface_name_on_the_exception_list_passes(tmp_path):
    # PROJECT_STATE.html is the kit's own example of a name that IS the
    # user-facing interface: the dashboard a stakeholder opens.
    need = "A stakeholder opens PROJECT_STATE.html and sees the plan's state."
    make_repo(tmp_path, need)
    proc = form(tmp_path)
    assert "PROJECT_STATE.html" in proc.stdout, "sanity: flagged without the list"
    make_repo(
        tmp_path,
        need,
        allow="# reviewed exceptions\n"
        "PROJECT_STATE.html — the dashboard IS the user-facing interface\n",
    )
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_an_allow_line_with_no_reason_separator_declares_nothing(tmp_path):
    # Fail-soft in the loud direction: a malformed entry cannot silence.
    need = "A stakeholder opens PROJECT_STATE.html and sees the plan's state."
    make_repo(tmp_path, need, allow="PROJECT_STATE.html\n")
    assert "PROJECT_STATE.html" in form(tmp_path).stdout


def test_acceptance_and_why_cells_are_exempt_by_sn033s_own_text(tmp_path):
    make_repo(
        tmp_path,
        "A reader recognizes the outcome they asked for.",
        extra_rows=(
            "[need.SN-051]\n"
            'kind = "core"\n'
            'priority = "M"\n'
            'need = """A team sees each check pass or fail."""\n'
            'why = """check.py and trace.py enforce it via --strict."""\n'
            'acceptance = """docs/gate reads DevBar-Reqs; SR-001 has a TC."""\n'
        ),
    )
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_example_rows_and_stakeholder_tier_cross_refs_are_ignored(tmp_path):
    make_repo(
        tmp_path,
        # An SN-### citation keeps the reader at the stakeholder tier — the SN
        # registry is the stakeholder's own document (the live SN-025 case).
        "The launcher that starts it is SN-034's obligation.",
        extra_rows=(
            "[need.SN-000]\n"
            'kind = "core"\n'
            'priority = "M"\n'
            'need = """Example row naming docs/example.md — ignored."""\n'
            'why = """example."""\n'
            'acceptance = """example."""\n'
        ),
    )
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_english_either_or_pairs_are_not_paths(tmp_path):
    make_repo(
        tmp_path,
        "A reviewer judges subjective/perceptual criteria and the "
        "requirement/test split without tooling.",
    )
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_the_live_registry_is_clean_at_zero_findings():
    # The WI's premise, held as a test: the check landed while the ratified
    # tier was clean (measured 2026-08-13, decision 7 rider 2), so the first
    # row to dirty the tier is the one that reports. A finding here is a real
    # regression of the registry, not of the checker.
    proc = form(ROOT)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_an_absent_needs_registry_is_a_clean_skip(tmp_path):
    (tmp_path / "docs").mkdir()
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean (0 need cell(s)" in proc.stdout, proc.stdout
