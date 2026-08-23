"""check_need_form.py — SN-033's declared need-cell form check (WI-454).

SN-033's approved acceptance commissions "a declared check [that] reports the
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
    "human_approval_through, as SR-137 and process.md §4 describe."
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
    for phrase in ("docs/status.md", "human_approval_through", "SR-137"):
        assert phrase in proc.stdout, "offending phrase not named: " + phrase
    # One finding per token, once: docs/status.md (path — its inner status.md
    # is NOT a second finding), human_approval_through, process.md, §4,
    # SR-137.
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
            'acceptance = """docs/stage reads DevStg-Reqs; SR-001 has a TC."""\n'
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


def test_a_one_level_dot_free_token_that_resolves_on_disk_is_a_path(tmp_path):
    # docs/archive carries no dot and one slash — the English-pair shape — but
    # it RESOLVES in the scanned tree, so it is an internal path (the round-1
    # adversarial review's driven find: the blanket exemption swallowed it).
    make_repo(tmp_path, "The design history lives in docs/archive for auditors.")
    (tmp_path / "docs" / "archive").mkdir()
    proc = form(tmp_path)
    assert "docs/archive" in proc.stdout, proc.stdout
    assert "internal path" in proc.stdout
    # The same token with NO target on disk keeps the English-pair exemption.
    make_repo(tmp_path, "The design history lives in docs2/archive for auditors.")
    assert "clean" in form(tmp_path).stdout


def test_a_url_is_suppressed_whole_however_path_shaped_its_tail(tmp_path):
    # The round-1 review's driven find: the lookbehind alone reported the
    # `test/docs/status.md` tail of a URL as an internal path. The whole URL
    # span is suppressed — for the path class AND the identifier class that
    # would re-match `status.md` inside it.
    make_repo(
        tmp_path,
        "Docs are published at https://example.test/docs/status.md for readers.",
    )
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_a_sentence_final_path_names_the_exact_phrase_so_its_exception_matches(
    tmp_path,
):
    # Round-2 review find: the segment charset allows dots, so a sentence-final
    # token dragged its full stop into the phrase (`docs/status.md.`) — the
    # report misnamed the token and its reviewed exception could never match.
    make_repo(tmp_path, "A user resumes work from docs/status.md.")
    proc = form(tmp_path)
    assert "'docs/status.md'" in proc.stdout, proc.stdout
    make_repo(
        tmp_path,
        "A user resumes work from docs/status.md.",
        allow="docs/status.md — the resume surface IS the user-facing entry\n",
    )
    assert "clean" in form(tmp_path).stdout
    # The corollary: a sentence-final English pair must not read its full stop
    # as a file suffix and false-positive as a path.
    make_repo(tmp_path, "A reviewer weighs each requirement/test.")
    assert "clean" in form(tmp_path).stdout


def test_a_scheme_less_www_address_is_suppressed_like_a_url(tmp_path):
    # Round-2 review find: `www.example.test/docs/status.md` reported as an
    # internal path although it is the same external reference as its
    # `https://` form. A genuine internal path in the SAME cell still reports.
    make_repo(tmp_path, "Docs live at www.example.test/docs/status.md for readers.")
    proc = form(tmp_path)
    assert "clean" in proc.stdout, proc.stdout
    make_repo(
        tmp_path,
        "Docs live at www.example.test/docs/guide.md, mirrored from "
        "docs/status.md nightly.",
    )
    proc = form(tmp_path)
    assert "'docs/status.md'" in proc.stdout, proc.stdout
    assert "guide.md" not in proc.stdout


def test_a_single_label_www_token_is_a_path_not_an_address(tmp_path):
    # Round-3 review find: the www. suppression swallowed a LOCAL path whose
    # first segment merely looks host-ish. A real scheme-less address carries
    # a second dot before its first slash (www.example.test); a single-label
    # `www.assets/logo.png` is repository internals and reports.
    make_repo(tmp_path, "Assets ship from www.assets/logo.png nightly.")
    (tmp_path / "www.assets").mkdir()
    proc = form(tmp_path)
    assert "'www.assets/logo.png'" in proc.stdout, proc.stdout


def test_a_url_span_stops_at_prose_delimiters(tmp_path):
    # Round-3 review find: the span's \S+ greediness swallowed a SEPARATE
    # genuine token abutting the URL through a comma. The span now stops at
    # `,`/`;`, so the neighbour reports while the URL itself stays exempt.
    make_repo(
        tmp_path,
        "See www.example.test/docs/status.md,docs/gate.md nightly; the "
        "mirror is https://example.test/a/b.md;docs/log.md holds the rest.",
    )
    proc = form(tmp_path)
    assert "'docs/gate.md'" in proc.stdout, proc.stdout
    assert "'docs/log.md'" in proc.stdout, proc.stdout
    assert "status.md'" not in proc.stdout
    assert "b.md'" not in proc.stdout


def test_a_present_but_vacuous_registry_is_reported_not_clean(tmp_path):
    # The round-1 review's driven find: an emptied registry scanned as a clean
    # tier, and at DevStg-Reqs nothing else in the harness hard-fails on it —
    # the false green SN-008 forbids, on exactly the registry this check
    # guards. Absent stays a clean skip; present-but-empty reports.
    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "stakeholder-needs.toml").write_text("", encoding="utf-8")
    proc = form(tmp_path)
    assert proc.returncode == 0, "warn-first: vacuous must not gate by default"
    assert "vacuous" in proc.stdout, proc.stdout
    assert "check_need_form: clean" not in proc.stdout
    assert form(tmp_path, "--strict").returncode == 1
    # Real rows that carry no `need` cell at all are the same emptied tier.
    (reg / "stakeholder-needs.toml").write_text(
        '[need.SN-050]\nkind = "core"\npriority = "M"\n'
        'why = """b."""\nacceptance = """c."""\n',
        encoding="utf-8",
    )
    assert "vacuous" in form(tmp_path).stdout


def test_an_example_only_registry_is_a_blank_form_not_a_vacuous_tier(tmp_path):
    # A fresh scaffold's registry holds only `-000` example rows: scanned=0,
    # but it is a blank form, not an emptied tier — the scaffold pays nothing.
    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "stakeholder-needs.toml").write_text(
        '[need.SN-000]\nkind = "core"\npriority = "M"\n'
        'need = """Example row naming docs/example.md — ignored."""\n'
        'why = """example."""\nacceptance = """example."""\n',
        encoding="utf-8",
    )
    proc = form(tmp_path)
    assert proc.returncode == 0
    assert "clean" in proc.stdout, proc.stdout


def test_the_live_registry_is_clean_at_zero_findings():
    # The WI's premise, held as a test: the check landed while the approved
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
