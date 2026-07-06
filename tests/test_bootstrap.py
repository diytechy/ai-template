"""Bootstrap must produce a scaffold that is green out of the box."""

from conftest import KIT, SCRIPTS, load_script, run_py


def test_scaffold_contains_expected_files(scaffold):
    for rel in [
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        ".gitignore",
        "pytest.ini",
        "docs/stack.ini",
        "docs/process.md",
        "docs/process-options.md",
        "docs/gate",
        "docs/gate-policy",
        "docs/privacy-check",
        "docs/push-policy",
        "docs/kit-profile",
        "docs/status.md",
        "docs/log.md",
        "docs/plan.md",
        "docs/architecture.md",
        "docs/requirements/system-requirements.csv",
        "docs/requirements/performance-budgets.csv",
        "docs/requirements/procurement.csv",
        "docs/requirements/assets.csv",
        "docs/test/test-cases.csv",
        "scripts/check.py",
        "scripts/check_privacy.py",
        "scripts/check_vendored.py",
        "scripts/gen_cases.py",
        ".githooks/pre-commit",
        ".githooks/commit-msg",
        ".githooks/pre-push",
        ".github/workflows/check.yml",
        "src/.gitkeep",
        "tests/.gitkeep",
        "README.md",
        "run.cmd",
        "run.sh",
        "run.command",
        "agent-resume.cmd",
        "agent-resume.sh",
        "agent-resume.command",
        "scripts/agent_loop.py",
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
        "the ~12k Gemini cap) — tighten another rule to pay for the growth".format(size)
    )


def test_status_is_working_surface_history_lives_in_log(scaffold):
    # Thread 36: status.md holds only what must be performed next; the history
    # sections (Gate Sign-offs, Audit log) live in the pointed-to docs/log.md,
    # headings preserved verbatim so downstream greps and the §5 prose survive.
    status = (scaffold / "docs" / "status.md").read_text(encoding="utf-8")
    for heading in ("## Gate Sign-offs", "## Audit log", "## Decisions log"):
        assert heading not in status, "history section left in status.md: " + heading
    assert "log.md" in status, "status.md must point at the history log"
    assert "blocks:" in status, "Open-items format must seed the blocks: clause"
    log = (scaffold / "docs" / "log.md").read_text(encoding="utf-8")
    for heading in ("## Gate Sign-offs", "## Audit log", "## Decisions log"):
        assert heading in log, "log.md must carry the history heading: " + heading
    assert "G-Final — Acceptance" in log  # the sign-off table moved intact


def test_plan_build_cadence_surfaces(scaffold):
    # WI-1.29: the plan/build cadence's scaffold surfaces. docs/plan.md is the
    # sequenced block list (PLAN writes, BUILD executes); status.md points at
    # it (the lean resume surface names, never holds, the plan); the launcher
    # templates seed the strong-plans/cheap-executes model-map example.
    plan = (scaffold / "docs" / "plan.md").read_text(encoding="utf-8")
    assert "Plan/build" in plan  # names the process-options cadence section
    assert "B-1" in plan  # the example block a fresh repo replaces
    assert "Done-when" in plan  # every block states an observable done-when
    assert "run-phase" in plan  # the bounce rule: exhausted/wrong -> PLAN
    status = (scaffold / "docs" / "status.md").read_text(encoding="utf-8")
    assert "plan.md" in status, "status.md must point at the work plan"
    for launcher in ("agent-resume.sh", "agent-resume.cmd"):
        text = (scaffold / launcher).read_text(encoding="utf-8")
        assert "PLAN=<strong-model>,BUILD=<cheap-model>" in text, (
            launcher + " must seed the plan/build model-map example"
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
    text = ga.read_text(encoding="utf-8")
    assert ".githooks/pre-commit text eol=lf" in text
    assert ".githooks/pre-push text eol=lf" in text


def test_scaffolded_process_doc_drops_template_meta_prose(scaffold):
    # Once copied, docs/process.md *is* the process doc — the "(template)" title
    # and "Copy this into a new repo" meta-prose read wrong and are stripped.
    proc = (scaffold / "docs" / "process.md").read_text(encoding="utf-8")
    assert "# Development Process" in proc
    assert "(template)" not in proc.splitlines()[0]
    assert "Copy this into a new" not in proc


def test_readme_scaffolded_with_project_name(scaffold):
    # The README skeleton is the human front door (WI-1.12): bootstrap fills
    # the one dynamic placeholder (project name = destination folder) and the
    # skeleton points at the launchers + the ladder for the kickoff agent to
    # build out from the brief.
    readme = (scaffold / "README.md").read_text(encoding="utf-8")
    assert "{{PROJECT_NAME}}" not in readme, "placeholder must be filled"
    assert readme.splitlines()[0] == "# " + scaffold.name
    assert "run.cmd" in readme  # points at the product launchers
    assert "onboard" in readme  # points at the onboarding ladder


def test_readme_vision_tag_and_needs_pointer(scaffold):
    # Thread 37: the README's ## Vision section (anchored by the singleton
    # PROJECT-VISION: token) is the purpose fact's canonical home; the needs
    # registry points at it with a real link, so check_docs mechanically keeps
    # the pointer from dangling (test_clean_scaffold_passes exercises that).
    readme = (scaffold / "README.md").read_text(encoding="utf-8")
    assert "## Vision" in readme
    assert "PROJECT-VISION:" in readme
    needs = (scaffold / "docs" / "requirements" / "stakeholder-needs.md").read_text(
        encoding="utf-8"
    )
    assert "](../../README.md#vision)" in needs


def test_readme_never_overwritten(tmp_path):
    # Adoption case: an existing README is the project's own front door —
    # bootstrap must skip it (same default-skip contract as every template).
    dest = tmp_path / "repo"
    dest.mkdir(parents=True)
    (dest / "README.md").write_text("my project's own readme", encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (dest / "README.md").read_text(encoding="utf-8")
    assert text == "my project's own readme"


def test_resync_does_not_regenerate_foreign_arch_map(tmp_path):
    # Re-sync against an adopted repo whose arch map is owned by a different
    # generator (e.g. the PowerShell port): bootstrap must not run the Python
    # generator over it — the generated block would be clobbered (the
    # FileBackup re-sync hit this). The initializer is gated on this run
    # having created docs/architecture.md.
    dest = tmp_path / "repo"
    (dest / "docs").mkdir(parents=True)
    sentinel = (
        "# Arch\n\n<!-- BEGIN GENERATED DEPENDENCY DIAGRAM -->\n"
        "_written by the ps1 port — SENTINEL_\n"
        "<!-- END GENERATED DEPENDENCY DIAGRAM -->\n"
    )
    (dest / "docs" / "architecture.md").write_text(sentinel, encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (dest / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "SENTINEL" in text, "re-sync must not regenerate a pre-existing map"


def test_run_launchers_ship_inert_with_edit_slots(scaffold):
    # The evaluator's rungs (WI-1.12): root double-clickable launchers, one per
    # platform, shipped inert (empty RUN_CMD) with a marked EDIT slot. The
    # macOS .command delegates to run.sh so the POSIX command lives once.
    cmd = (scaffold / "run.cmd").read_text(encoding="utf-8")
    assert 'set "RUN_CMD="' in cmd, "run.cmd must ship with an empty RUN_CMD"
    assert "EDIT FOR YOUR PROJECT" in cmd
    sh = (scaffold / "run.sh").read_text(encoding="utf-8")
    assert 'RUN_CMD=""' in sh, "run.sh must ship with an empty RUN_CMD"
    assert "EDIT FOR YOUR PROJECT" in sh
    command = (scaffold / "run.command").read_text(encoding="utf-8")
    assert "./run.sh" in command, ".command must delegate to run.sh"
    assert "RUN_CMD=" not in command, ".command must not carry a third copy"


def test_agent_resume_launchers_ship_inert_with_edit_slots(scaffold):
    # The work-resume counterpart of run.* (Thread 33): root agent launchers
    # over scripts/agent_loop.py, shipped inert (empty AGENT_CMD) with a
    # marked EDIT slot and an explicit consent note; .command delegates to
    # .sh so the POSIX slots live once.
    cmd = (scaffold / "agent-resume.cmd").read_text(encoding="utf-8")
    assert 'set "AGENT_CMD="' in cmd, "agent-resume.cmd must ship inert"
    assert "EDIT FOR YOUR PROJECT" in cmd
    assert "CONSENT" in cmd
    sh = (scaffold / "agent-resume.sh").read_text(encoding="utf-8")
    assert 'AGENT_CMD=""' in sh, "agent-resume.sh must ship inert"
    assert "CONSENT" in sh
    command = (scaffold / "agent-resume.command").read_text(encoding="utf-8")
    assert "./agent-resume.sh" in command, ".command must delegate to .sh"
    assert 'AGENT_CMD=""' not in command, ".command must not carry a third copy"
    engine = (scaffold / "scripts" / "agent_loop.py").read_text(encoding="utf-8")
    assert "run-state" in engine  # the engine, not a stub


def test_agents_choice_seeds_agent_resume_slots(tmp_path):
    # --agents claude seeds the launcher EDIT slots with that agent's example
    # command (the consent line: the seeded AGENT_CMD carries the bypass flag
    # the launcher header explains). The slots stay repo-owned EDIT blocks.
    dest = tmp_path / "repo"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--agents", "claude"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    sh = (dest / "agent-resume.sh").read_text(encoding="utf-8")
    assert 'AGENT_CMD="claude -p {prompt} --model {model}' in sh
    # Strong tier is the seeded default (driver sessions are gate-bearing);
    # cheaper phases are the model map's job.
    assert 'AGENT_MODEL="opus"' in sh
    cmd = (dest / "agent-resume.cmd").read_text(encoding="utf-8")
    assert 'set "AGENT_CMD=claude -p {prompt}' in cmd
    assert "seeded agent-resume launchers" in proc.stdout


def test_default_scaffold_leaves_agent_resume_unseeded(scaffold):
    # No agent chosen (the CI-safe default) -> the slots stay empty; the
    # launchers are discoverable but inert.
    sh = (scaffold / "agent-resume.sh").read_text(encoding="utf-8")
    assert 'AGENT_CMD=""' in sh


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


# --- Privacy-check toggle (Thread 38 -> identity/privacy reframe) --------------


def _policy_lines(path):
    return [
        ln
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]


def test_privacy_check_defaults_to_false(scaffold):
    # The scaffolded toggle is `false` — the privacy gate is off by default, so
    # existing adopters and default scaffolds see zero change (the always-on
    # secrets floor still runs regardless).
    assert _policy_lines(scaffold / "docs" / "privacy-check") == ["false"]


def test_privacy_check_flag_sets_toggle(tmp_path):
    # --privacy-check sets the toggle at repo creation, keeping the template's
    # explanatory header above the value.
    dest = tmp_path / "repo"
    proc = run_py(
        [
            SCRIPTS / "bootstrap.py",
            "--dest",
            dest,
            "--privacy-check",
            "true",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    policy = dest / "docs" / "privacy-check"
    assert _policy_lines(policy) == ["true"]
    assert policy.read_text(encoding="utf-8").startswith("#"), "header kept"


def test_setup_scripts_advise_on_privacy_not_pin_identity():
    # Identity is user-owned: the setup launchers no longer set an author
    # identity. They read docs/privacy-check and advise (via check_privacy
    # --author) when a private author would be blocked; they must never touch
    # global git config.
    for name in ("setup.sh", "setup.ps1"):
        text = (KIT / "scripts" / name).read_text(encoding="utf-8")
        assert "privacy-check" in text, name + " must read the privacy toggle"
        assert "git config --global" not in text, name + " must stay repo-local"


# --- Agent selection & the skills layer (WI-1.9) -----------------------------


def _bootstrap(tmp_path, *extra):
    dest = tmp_path / "repo"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest, *extra], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return dest


def test_non_interactive_default_materializes_no_agent_layer(tmp_path):
    # The property the spec pins: run non-interactively with NO --agents flag and
    # the scaffold is the historical, agent-neutral one — no .claude/.gemini dirs,
    # no skills, no setup note. (conftest.run_py closes stdin, so the omitted-flag
    # path takes its 'none' default exactly as CI would.)
    dest = _bootstrap(tmp_path)
    assert not (dest / ".claude").exists(), "default must not materialize .claude"
    assert not (dest / ".gemini").exists(), "default must not materialize .gemini"
    status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
    assert "<!-- agent-setup -->" not in status, "default must add no setup note"


def test_explicit_agents_none_matches_default(tmp_path):
    # --agents none is the same agent-neutral result, just stated explicitly.
    dest = _bootstrap(tmp_path, "--agents", "none")
    assert not (dest / ".claude").exists()
    assert not (dest / ".gemini").exists()


def test_agents_claude_materializes_kit_skills_and_inert_hook(tmp_path):
    dest = _bootstrap(tmp_path, "--agents", "claude")
    skills = dest / ".claude" / "skills"
    assert skills.is_dir(), "claude selection must materialize .claude/skills"
    # Only kit-scope skills ship downstream; the this-repo ones must NOT.
    names = {p.name for p in skills.iterdir()}
    assert {"registry-hygiene", "downstream-resync", "gate-advance"} <= names
    assert "byte-budget-guard" not in names, "this-repo skill must not ship"
    assert "session-protocol" not in names, "this-repo skill must not ship"
    # Each materialized skill keeps its neutral SKILL.md verbatim.
    assert (skills / "registry-hygiene" / "SKILL.md").exists()
    # The hook config is copied INERT (as an example), never a live settings.json.
    assert (dest / ".claude" / "settings.json.example").exists()
    assert not (dest / ".claude" / "settings.json").exists()
    # Gemini gets nothing for a claude-only selection.
    assert not (dest / ".gemini").exists()
    # The choice + date is recorded in status.md.
    status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
    assert "<!-- agent-setup -->" in status
    assert "agents=`claude`" in status


def test_agents_both_materializes_for_both(tmp_path):
    dest = _bootstrap(tmp_path, "--agents", "both")
    for agent_dir in (".claude", ".gemini"):
        skills = dest / agent_dir / "skills"
        assert skills.is_dir(), agent_dir + " must get skills"
        assert (skills / "gate-advance" / "SKILL.md").exists()
        assert (dest / agent_dir / "settings.json.example").exists()


def test_scaffold_with_agents_still_green(tmp_path):
    # Materializing the agent layer must not break the out-of-the-box harness.
    dest = _bootstrap(tmp_path, "--agents", "both")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=dest)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=dest
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_scope_matcher_is_tag_intersection():
    boot = load_script("bootstrap")
    # `any` on an axis always matches; a specific value matches only its members.
    py_only = {"stacks": ["python"], "domains": ["any"]}
    assert boot.matches_scope(py_only, "python", "any", False)
    assert not boot.matches_scope(py_only, "go", "any", False)
    # A skipped answer ("") never filters.
    assert boot.matches_scope(py_only, "", "web", False)
    any_skill = {"stacks": ["any"], "domains": ["any"]}
    assert boot.matches_scope(any_skill, "rust", "hardware", True)


def test_select_skills_returns_only_kit_scope():
    boot = load_script("bootstrap")
    chosen = {n for n, _ in boot.select_skills("any", "any", False)}
    assert {"registry-hygiene", "downstream-resync", "gate-advance"} <= chosen
    assert "byte-budget-guard" not in chosen
    assert "session-protocol" not in chosen


def test_skills_index_is_fresh():
    # The generated INDEX.csv must match the SKILL.md files (like arch-map --check).
    proc = run_py([SCRIPTS / "gen_skills_index.py", "--check"], cwd=KIT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
