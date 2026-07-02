"""Bootstrap must produce a scaffold that is green out of the box."""

from conftest import KIT, SCRIPTS, run_py


def test_scaffold_contains_expected_files(scaffold):
    for rel in [
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        ".gitignore",
        "pytest.ini",
        "docs/process.md",
        "docs/process-options.md",
        "docs/gate",
        "docs/status.md",
        "docs/architecture.md",
        "docs/requirements/system-requirements.csv",
        "docs/requirements/performance-budgets.csv",
        "docs/requirements/procurement.csv",
        "docs/requirements/assets.csv",
        "docs/test/test-cases.csv",
        "scripts/check.py",
        "scripts/gen_cases.py",
        ".github/workflows/check.yml",
        "src/.gitkeep",
        "tests/.gitkeep",
    ]:
        assert (scaffold / rel).exists(), "missing from scaffold: " + rel


def test_agents_guide_is_canonical_and_stubs_point_at_it(scaffold):
    # AGENTS.md carries the full guide; CLAUDE.md/GEMINI.md are thin stubs that
    # point back at it (single source of truth — Thread 0a).
    agents = (scaffold / "AGENTS.md").read_text(encoding="utf-8")
    assert "How we work here (the process)" in agents  # a full-guide section
    assert "Working agreement" in agents
    for stub_name in ("CLAUDE.md", "GEMINI.md"):
        stub = (scaffold / stub_name).read_text(encoding="utf-8")
        assert "AGENTS.md" in stub, stub_name + " should point at AGENTS.md"
        # The stub must not duplicate the full guide.
        assert "Working agreement" not in stub, stub_name + " duplicates the guide"


def test_agents_template_stays_within_size_budget():
    # Gemini's AGENTS.md support truncates near ~12k chars, and a downstream
    # project must still fill the Project section and add its own rules. The
    # shipped template therefore keeps >=2k of headroom; a kit thread that
    # grows it past this budget must pay by tightening elsewhere (the file's
    # own Customizing note states the same rule for downstream editors).
    size = len((KIT / "AGENTS.template.md").read_bytes())
    assert size <= 10_000, (
        "AGENTS.template.md is {} bytes; budget is 10,000 (>=2k headroom under "
        "the ~12k Gemini cap) — tighten another rule to pay for the growth".format(
            size
        )
    )


def test_fresh_scaffold_passes_archmap_check_and_trace(scaffold):
    # Bootstrap runs the generators itself, so --check must pass immediately —
    # a fresh repo must not start with a failing harness.
    proc = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout


def test_scaffold_architecture_has_generated_diagram_block(scaffold):
    arch = (scaffold / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "BEGIN GENERATED DEPENDENCY DIAGRAM" in arch
    # Empty src at bootstrap time -> the spliced placeholder, not the template's.
    assert "(no source scanned)" in arch


def test_scaffold_stamps_kit_version(scaffold):
    # docs/kit-version records the kit commit the scaffold came from, so a later
    # re-sync is a diff against kit HEAD, not a guess (ADOPTING.md §6).
    stamp = scaffold / "docs" / "kit-version"
    assert stamp.exists(), "bootstrap must write docs/kit-version"
    text = stamp.read_text(encoding="utf-8")
    assert "ADOPTING.md" in text  # points the reader at the re-sync guidance
    # The last non-comment line is the identity: a short SHA (+ optional -dirty
    # + date) or the explicit unknown marker for a non-git kit copy.
    ident = [ln for ln in text.splitlines() if ln and not ln.startswith("#")][-1]
    assert ident.strip(), "kit-version must carry a non-empty identity line"


def test_scaffold_pins_hook_line_endings(scaffold):
    # The sh-based git hook breaks under Windows autocrlf without an eol=lf pin;
    # the scaffolded .gitattributes must carry that rule (friction from the pilot).
    ga = scaffold / ".gitattributes"
    assert ga.exists(), "bootstrap must scaffold .gitattributes"
    assert ".githooks/pre-commit text eol=lf" in ga.read_text(encoding="utf-8")


def test_scaffolded_process_doc_drops_template_meta_prose(scaffold):
    # Once copied, docs/process.md *is* the process doc — the "(template)" title
    # and "Copy this into a new repo" meta-prose read wrong and are stripped.
    proc = (scaffold / "docs" / "process.md").read_text(encoding="utf-8")
    assert "# Development Process" in proc
    assert "(template)" not in proc.splitlines()[0]
    assert "Copy this into a new" not in proc


def test_dry_run_writes_nothing(tmp_path):
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", tmp_path / "repo", "--dry-run"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not (tmp_path / "repo").exists()


def test_rerun_skips_existing_files(scaffold):
    (scaffold / "CLAUDE.md").write_text("customized", encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", scaffold], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (scaffold / "CLAUDE.md").read_text(encoding="utf-8") == "customized"
