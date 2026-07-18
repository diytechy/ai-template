"""S7: the per-agent skill fan-out stays a checked, one-command-refreshable copy
of the ONE neutral source (SR-025 / LLR-043 / TC-045).

The kit fans `project-trajectory/skills/<name>/` out to `.claude/skills/`,
`.gemini/skills/`, and `.agents/skills/` as byte-identical copies. These tests
pin the drift gate (`gen_skills_index.py --check-agents`), the one-command
refresh (`bootstrap.py --sync`), and `.agents/` as a first-class bootstrap
target (`--agents codex`).
"""

from conftest import KIT, SCRIPTS, load_script, run_py

SOURCE = KIT / "skills"
GEN = SCRIPTS / "gen_skills_index.py"
BOOT = SCRIPTS / "bootstrap.py"


def _mk_source(tmp, names=("alpha", "beta")):
    """A synthetic neutral source dir with one SKILL.md per skill (LF bytes)."""
    src = tmp / "src-skills"
    for n in names:
        d = src / n
        d.mkdir(parents=True)
        (d / "SKILL.md").write_bytes(
            "---\nname: {0}\ndescription: x\nscope: kit\n---\nbody {0}\n".format(
                n
            ).encode("utf-8")
        )
    return src


def _copy_tree(src_skill, dst_skill):
    dst_skill.mkdir(parents=True, exist_ok=True)
    for f in src_skill.iterdir():
        if f.is_file():
            (dst_skill / f.name).write_bytes(f.read_bytes())


# --- the drift gate: gen_skills_index --check-agents -------------------------


def test_check_agents_vacuous_without_per_agent_dirs(tmp_path):
    # No .claude/.gemini/.agents under root -> nothing to check -> pass.
    src = _mk_source(tmp_path)
    proc = run_py(
        [GEN, "--check-agents", "--source", src, "--root", tmp_path], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_check_agents_vacuous_without_source(tmp_path):
    # A per-agent dir exists but there's no neutral source (a scaffold's case) ->
    # vacuous: there is nothing in-repo to be identical to.
    d = tmp_path / ".claude" / "skills" / "alpha"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text("x", encoding="utf-8")
    proc = run_py(
        [GEN, "--check-agents", "--source", tmp_path / "nope", "--root", tmp_path],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_check_agents_passes_on_identical_copies(tmp_path):
    src = _mk_source(tmp_path)
    for agentdir in (".claude/skills", ".agents/skills"):
        for n in ("alpha", "beta"):
            _copy_tree(src / n, tmp_path / agentdir / n)
    proc = run_py(
        [GEN, "--check-agents", "--source", src, "--root", tmp_path], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_check_agents_fails_on_drift(tmp_path):
    src = _mk_source(tmp_path)
    _copy_tree(src / "alpha", tmp_path / ".claude/skills/alpha")
    (tmp_path / ".claude/skills/alpha/SKILL.md").write_text(
        "hand edited\n", encoding="utf-8"
    )
    proc = run_py(
        [GEN, "--check-agents", "--source", src, "--root", tmp_path], cwd=tmp_path
    )
    assert proc.returncode != 0
    assert "drifted" in (proc.stdout + proc.stderr).lower()


def test_check_agents_subset_is_fine(tmp_path):
    # A per-agent dir carrying only a SUBSET of source skills passes — a source
    # skill missing from the copy is legitimate scope-matched materialization,
    # NOT drift (the documented missing-skill decision).
    src = _mk_source(tmp_path, names=("alpha", "beta"))
    _copy_tree(src / "alpha", tmp_path / ".gemini/skills/alpha")  # beta absent
    proc = run_py(
        [GEN, "--check-agents", "--source", src, "--root", tmp_path], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_check_agents_is_byte_exact_crlf_is_drift(tmp_path):
    # Binary-safe: a CRLF-vs-LF-only difference is real drift (not silently equal),
    # and byte-identical copies pass. In-process for a precise byte assertion.
    gen = load_script("gen_skills_index")
    src = tmp_path / "src-skills" / "alpha"
    src.mkdir(parents=True)
    (src / "SKILL.md").write_bytes(b"line1\nline2\n")
    copy = tmp_path / ".claude" / "skills" / "alpha"
    copy.mkdir(parents=True)
    (copy / "SKILL.md").write_bytes(b"line1\nline2\n")  # identical bytes
    drifts, orphans, checked = gen.check_agent_sync(tmp_path / "src-skills", tmp_path)
    assert (drifts, checked) == ([], 1)
    (copy / "SKILL.md").write_bytes(b"line1\r\nline2\r\n")  # CRLF: real drift
    drifts, orphans, checked = gen.check_agent_sync(tmp_path / "src-skills", tmp_path)
    assert drifts and checked == 1


def test_check_agents_orphan_warns_not_fails(tmp_path):
    # A copy whose skill no longer exists in source is surfaced as a WARN, never a
    # hard fail (it can't be fixed by --sync — the fix is a manual removal).
    src = _mk_source(tmp_path, names=("alpha",))
    _copy_tree(src / "alpha", tmp_path / ".claude/skills/alpha")
    orphan = tmp_path / ".claude" / "skills" / "ghost"
    orphan.mkdir(parents=True)
    (orphan / "SKILL.md").write_text("no source\n", encoding="utf-8")
    proc = run_py(
        [GEN, "--check-agents", "--source", src, "--root", tmp_path], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphan" in (proc.stdout + proc.stderr).lower()


# --- the one-command refresh: bootstrap --sync -------------------------------


def test_sync_refreshes_only_skills_subtree(tmp_path):
    # --sync refreshes a drifted per-agent copy to byte-identity with the KIT
    # source, and NEVER touches a file outside <agent>/skills/<name>/.
    name = "registry-hygiene"  # a real kit-scope skill
    claude = tmp_path / ".claude" / "skills" / name
    claude.mkdir(parents=True)
    (claude / "SKILL.md").write_text("STALE - hand edited\n", encoding="utf-8")
    sentinel_out = tmp_path / ".claude" / "settings.json"  # project-owned
    sentinel_out.write_text("my own settings", encoding="utf-8")
    sentinel_in = tmp_path / ".claude" / "skills" / "keepme.txt"  # not a skill dir
    sentinel_in.write_text("keep", encoding="utf-8")

    proc = run_py([BOOT, "--dest", tmp_path, "--sync"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (claude / "SKILL.md").read_bytes() == (
        SOURCE / name / "SKILL.md"
    ).read_bytes()
    assert sentinel_out.read_text(encoding="utf-8") == "my own settings"
    assert sentinel_in.read_text(encoding="utf-8") == "keep"


def test_sync_is_vacuous_without_per_agent_dirs(tmp_path):
    proc = run_py([BOOT, "--dest", tmp_path, "--sync"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 per-agent skill file" in proc.stdout


def test_drifted_copy_fails_and_sync_restores(tmp_path):
    # TC-045 headline, over the real kit source + the production commands: a
    # drifted copy fails --check-agents; --sync restores byte-identity; green.
    name = "gate-advance"
    claude = tmp_path / ".claude" / "skills" / name
    claude.mkdir(parents=True)
    (claude / "SKILL.md").write_text("drifted\n", encoding="utf-8")
    bad = run_py(
        [GEN, "--check-agents", "--source", SOURCE, "--root", tmp_path], cwd=tmp_path
    )
    assert bad.returncode != 0, bad.stdout + bad.stderr
    fix = run_py([BOOT, "--dest", tmp_path, "--sync"], cwd=tmp_path)
    assert fix.returncode == 0, fix.stdout + fix.stderr
    good = run_py(
        [GEN, "--check-agents", "--source", SOURCE, "--root", tmp_path], cwd=tmp_path
    )
    assert good.returncode == 0, good.stdout + good.stderr


# --- .agents/ as a first-class bootstrap target: --agents codex --------------


def test_bootstrap_agents_codex_populates_dot_agents(tmp_path):
    dest = tmp_path / "repo"
    proc = run_py([BOOT, "--dest", dest, "--agents", "codex"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    skills = dest / ".agents" / "skills"
    assert skills.is_dir(), "codex selection must materialize .agents/skills"
    names = {p.name for p in skills.iterdir()}
    # kit-scope skills materialize; this-repo skills do not (same rule as claude).
    assert {"registry-hygiene", "downstream-resync", "gate-advance"} <= names
    assert "session-protocol" not in names and "byte-budget-guard" not in names
    # Each copy is byte-identical to the neutral source.
    assert (skills / "registry-hygiene" / "SKILL.md").read_bytes() == (
        SOURCE / "registry-hygiene" / "SKILL.md"
    ).read_bytes()
    # codex ships no hook config -> no inert example; a codex-only run adds no
    # .claude/.gemini.
    assert not (dest / ".agents" / "settings.json.example").exists()
    assert not (dest / ".claude").exists() and not (dest / ".gemini").exists()


def test_codex_is_a_first_class_agent_target():
    boot = load_script("bootstrap")
    assert "codex" in boot.AGENT_CHOICES
    assert boot.AGENTS["codex"]["skills_dir"] == ".agents/skills"
    assert boot.selected_agents("codex") == ["codex"]
    # 'both' keeps its historical meaning (claude + gemini).
    assert boot.selected_agents("both") == ["claude", "gemini"]
