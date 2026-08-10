"""trace.py's optional coordinator repo-delegation registry (Thread 20,
MULTI_REPO.md): REPO-### rows live off the SN->SR->LLR->TC spine (the multi-repo
layer) but stay traceable *within the coordinator repo* — each DelegatedSRs value
back-links a real coordinator SR, and a malformed REPO id or a dangling
delegation fails --strict. The registry is optional and coordinator-only: it is
NOT scaffolded by bootstrap, an absent file is a no-op, and a leftover REPO-000
never blocks a gate. An external/reused part referenced only via the IF-###
catalog may delegate nothing, so an empty back-link is allowed here (unlike PB).
The registry was formerly modules.csv / MOD-### — the legacy file + ids are
still read (never breaking), pinned below.
"""

from conftest import make_minimal_project, run_py, record_ids

REPO_HEADER = "REPO-ID,Name,Repo,DelegatedSRs,Version,Type,Owner,Notes\n"
ROW = "{rid},widget,https://example.com/org/widget,{delegated},v1,owned,Integration,note\n"
LEGACY_HEADER = "MOD-ID,Module,Repo,DelegatedSRs,Version,Type,Owner,Notes\n"


def repo_path(root):
    return root / "docs" / "requirements" / "repos.csv"


def legacy_path(root):
    return root / "docs" / "requirements" / "modules.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_repos(root, *rows):
    repo_path(root).write_text(REPO_HEADER + "".join(rows), encoding="utf-8")
    record_ids(root)


def write_legacy_modules(root, *rows):
    legacy_path(root).write_text(LEGACY_HEADER + "".join(rows), encoding="utf-8")
    record_ids(root)


def test_registry_not_scaffolded_and_absent_file_is_noop(scaffold):
    # repos.csv is the coordinator-only multi-repo layer: bootstrap does not lay
    # it down, and a single-repo project's trace run must ignore its absence.
    make_minimal_project(scaffold)
    assert not repo_path(scaffold).exists()
    assert not legacy_path(scaffold).exists()
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "repos=" not in proc.stdout


def test_clean_repo_delegating_real_sr_passes(scaffold):
    make_minimal_project(scaffold)
    write_repos(scaffold, ROW.format(rid="REPO-001", delegated="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "repos=1 delegation-findings=0" in proc.stdout


def test_repo_delegating_unknown_sr_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_repos(scaffold, ROW.format(rid="REPO-001", delegated="SR-999"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "REPO REPO-001 delegates unknown SR-999" in report_of(scaffold)


def test_repo_with_empty_delegation_passes(scaffold):
    # An external/reused part referenced only via the interface catalog delegates
    # no functional SR, so an empty DelegatedSRs is allowed (unlike PB's Refs).
    make_minimal_project(scaffold)
    write_repos(scaffold, ROW.format(rid="REPO-001", delegated=""))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "repos=1 delegation-findings=0" in proc.stdout


def test_malformed_repo_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_repos(scaffold, ROW.format(rid="REPO-XX", delegated="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "REPO id 'REPO-XX' is malformed" in report_of(scaffold)


def test_placeholder_repo_row_is_inert(scaffold):
    # A REPO-000 example row (the template's placeholder) must never block a gate,
    # even under --no-placeholders, the same stance as interfaces.csv / PB-000.
    make_minimal_project(scaffold)
    write_repos(scaffold, ROW.format(rid="REPO-000", delegated="SR-000"))
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With no real REPO rows, no delegation section/counts are emitted at all.
    assert "repos=" not in proc.stdout


# --- legacy modules.csv / MOD-### back-compat (the pre-rename form) --------------


def test_legacy_modules_csv_still_read(scaffold):
    # A pre-rename adoption keeps validating unchanged: modules.csv + MOD- ids.
    make_minimal_project(scaffold)
    write_legacy_modules(
        scaffold,
        "MOD-001,widget,https://example.com/org/widget,SR-001,v1,owned,Integration,note\n",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "repos=1 delegation-findings=0" in proc.stdout


def test_legacy_module_dangling_delegation_still_fails(scaffold):
    make_minimal_project(scaffold)
    write_legacy_modules(
        scaffold,
        "MOD-001,widget,https://example.com/org/widget,SR-999,v1,owned,Integration,note\n",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "MOD MOD-001 delegates unknown SR-999" in report_of(scaffold)


def test_both_files_coexist_during_migration(scaffold):
    # Mid-migration a coordinator may hold repos.csv AND the legacy modules.csv;
    # both are read into one delegation set.
    make_minimal_project(scaffold)
    write_repos(scaffold, ROW.format(rid="REPO-001", delegated="SR-001"))
    write_legacy_modules(
        scaffold,
        "MOD-002,gadget,https://example.com/org/gadget,SR-001,v1,owned,Integration,note\n",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "repos=2 delegation-findings=0" in proc.stdout


def test_optional_columns_do_not_break_strict_schema(scaffold):
    # The Delegated/ParentRef markers and the delegation registry are schema-safe:
    # a coordinator SR carrying an optional Delegated column still passes
    # --strict-schema (the optional-column tolerance, like Area/Lifecycle/PB).
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    text = srs.read_text(encoding="utf-8")
    header, row = text.splitlines()[0], text.splitlines()[1]
    srs.write_text(header + ",Delegated\n" + row + ",REPO-001\n", encoding="utf-8")
    write_repos(scaffold, ROW.format(rid="REPO-001", delegated="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
